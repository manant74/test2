"""
Gemini Client - Wrapper for Google Gemini API
Handles authentication, error management, and timeout configuration
"""

import google.generativeai as genai
import streamlit as st
from typing import Optional


class GeminiClient:
    """Wrapper for Google Gemini API with error handling and timeout management"""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize Gemini client with API key from Streamlit secrets
        
        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout
        self.api_key = st.secrets.get("GEMINI_API_KEY")
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                st.warning(f"Errore nella configurazione Gemini API: {e}")
                self.model = None
        else:
            st.warning("GEMINI_API_KEY non configurata nei secrets")
    
    def is_configured(self) -> bool:
        """
        Check if Gemini API is properly configured
        
        Returns:
            bool: True if API is configured and ready to use
        """
        return self.model is not None
    
    def generate_text(self, prompt: str) -> Optional[str]:
        """
        Generate text using Gemini API with error handling and timeout
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Generated text or None if error occurs
            
        Raises:
            ValueError: If Gemini API is not configured
            TimeoutError: If request exceeds timeout limit
        """
        if not self.is_configured():
            raise ValueError("Gemini API non configurata. Verifica GEMINI_API_KEY nei secrets.")
        
        try:
            # Configure generation with timeout
            generation_config = genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                max_output_tokens=1024,
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                request_options={'timeout': self.timeout}
            )
            
            return response.text.strip()
            
        except TimeoutError as e:
            st.error(f"Timeout nella richiesta Gemini (>{self.timeout}s): {e}")
            return None
        except Exception as e:
            st.error(f"Errore nella generazione testo Gemini: {e}")
            return None
