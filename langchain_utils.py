import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class InterviewCoach:
    def __init__(self):
        self.api_key = None
        self.chain = None

    def configure(self, api_key):
        self.api_key = api_key
        # Initialize LangChain model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.7
        )
        
        # Define the system prompt template
        template = """
        You are an expert technical interviewer.
        
        Context / Document Content:
        {resume_text}
        
        Target Role / Job Description:
        {job_desc}
        
        Your Goal:
        Conduct a structured interview based on the provided Context/Document.
        - If the document is a Resume, interview the candidate for the Target Role, focusing on gaps and skills.
        - If the document is a specific topic (e.g., technical paper, article), interview the user about their understanding of the concepts within that document.
        - Start by introducing yourself and asking a relevant initial question based on the document's content.
        - Keep the conversation professional and engaging.
        
        Current Interview State:
        - If history is empty, start the interview.
        - If candidate answered, provide brief feedback (1-2 sentences) then ask the next question.
        - Conduct EXACTLY 5 questions.
        - After the 5th answer is received, immediately stop asking questions, analyze the conversation, and provide the final verdict.
        - If the status is 'finished', do not ask more questions.
        
        IMPORTANT: Respond in valid JSON format ONLY.
        Structure:
        {{
            "message": "content of your response to the user",
            "status": "ongoing" or "finished",
            "score": <float 1-10 rating of the LAST answer only, null if start>,
            "final_score": <float 1-10 rating of overall performance, null if not finished>,
            "verdict": "SELECTED" or "NOT SELECTED" (null if not finished)
        }}

        Chat History:
        {history}
        
        Candidate: {user_input}
        
        Interviewer (JSON):
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["job_desc", "resume_text", "history", "user_input"]
        )
        
        # Create chain: Prompt -> LLM -> StrParser
        self.chain = prompt | llm | StrOutputParser()

    def get_response(self, role, user_input=None, history=None, resume_text="N/A", job_desc="N/A"):
        """
        Interacts with Google Gemini via LangChain to conduct the interview.
        """
        # Fallback
        if not self.api_key or not self.chain:
             return {"message": "⚠️ API Key missing.", "status": "ongoing"}

        try:
            # Format history string
            history_str = ""
            if history:
                for msg in history:
                    role_label = "Candidate" if msg['role'] == 'user' else "Interviewer"
                    history_str += f"{role_label}: {msg['content']}\n"
            
            # Run the chain
            response_text = self.chain.invoke({
                "job_desc": job_desc if job_desc else f"Role: {role}",
                "resume_text": resume_text if resume_text else "Not provided",
                "history": history_str,
                "user_input": user_input if user_input else ""
            })
            
            # Parse JSON
            # Clean potential markdown code blocks if the model adds them
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            
            try:
                data = json.loads(clean_text)
                return data
            except json.JSONDecodeError:
                return {
                    "message": clean_text,
                    "status": "ongoing",
                    "score": None
                }

        except Exception as e:
            return {
                "message": f"Error connecting to AI via LangChain: {str(e)}",
                "status": "ongoing",
                "score": None
            }

