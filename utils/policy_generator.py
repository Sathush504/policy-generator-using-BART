"""Policy generation using OpenAI GPT"""

import openai
import os
from typing import Optional

class PolicyGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key (if None, reads from environment)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def generate_adapted_policy(self, 
                               original_summary: str,
                               scenario: dict,
                               temperature: float = 0.7,
                               max_tokens: int = 2000,
                               additional_context: str = "") -> str:
        """
        Generate adapted policy based on scenario
        
        Args:
            original_summary: Summary of original policy
            scenario: Scenario configuration dictionary
            temperature: Creativity parameter (0-1)
            max_tokens: Maximum length of generated policy
            additional_context: Additional user-provided context
            
        Returns:
            Generated adapted policy text
        """
        if not self.client:
            return "Error: OpenAI API key not configured. Please add your API key to the .env file."
        
        # Build comprehensive prompt
        prompt = self._build_prompt(original_summary, scenario, additional_context)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert policy analyst and writer specializing in adapting government policies for different contexts and scenarios."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating policy: {str(e)}"
    
    def _build_prompt(self, summary: str, scenario: dict, 
                     additional_context: str) -> str:
        """Build detailed prompt for policy generation"""
        
        constraints_text = "\n".join(f"- {c}" for c in scenario["constraints"])
        priorities_text = "\n".join(f"- {p}" for p in scenario["priorities"])
        
        prompt = f"""
You are tasked with adapting a digital government policy for a specific scenario.

ORIGINAL POLICY SUMMARY:
{summary}

ADAPTATION SCENARIO: {scenario['name']}
Description: {scenario['description']}

CONSTRAINTS TO ADDRESS:
{constraints_text}

PRIORITIES TO EMPHASIZE:
{priorities_text}

TARGET AUDIENCE: {scenario['audience']}
TONE: {scenario['tone']}

{f"ADDITIONAL CONTEXT: {additional_context}" if additional_context else ""}

INSTRUCTIONS:
1. Analyze the original policy summary carefully
2. Adapt the policy to address the specific constraints listed above
3. Emphasize and expand on the priorities relevant to this scenario
4. Maintain the core objectives while tailoring implementation strategies
5. Use the specified tone and consider the target audience
6. Structure the output with clear sections:
   - Executive Summary
   - Adapted Goals & Objectives
   - Key Strategies & Measures
   - Implementation Considerations
   - Risk Mitigation
   - Success Metrics

Generate a comprehensive adapted policy document (approximately 500-800 words).
"""
        
        return prompt
    
    def compare_policies(self, original: str, adapted: str, 
                        scenario_name: str) -> str:
        """
        Generate comparative analysis between original and adapted policies
        
        Args:
            original: Original policy text
            adapted: Adapted policy text
            scenario_name: Name of adaptation scenario
            
        Returns:
            Comparative analysis text
        """
        if not self.client:
            return "Error: OpenAI API key not configured."
        
        prompt = f"""
Compare the following two policy versions and provide a detailed analysis:

ORIGINAL POLICY:
{original[:1500]}

ADAPTED POLICY ({scenario_name}):
{adapted[:1500]}

Provide a structured comparison covering:
1. Key Differences in Approach
2. New Elements Introduced
3. Modified Priorities
4. Implementation Changes
5. Potential Impact Differences

Keep the analysis concise but insightful (300-400 words).
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a policy analysis expert specializing in comparative policy analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating comparison: {str(e)}"