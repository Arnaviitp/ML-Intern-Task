"""
Content filtering and safety checks for ethical AI usage
"""

import re
from typing import List, Tuple


class ContentFilter:
    """Content filter for detecting inappropriate prompts"""
    
    def __init__(self):
        # Blocked keywords (simplified list - expand based on requirements)
        self.blocked_keywords = [
            # Violence
            "violence", "gore", "blood", "death", "murder", "weapon",
            # Explicit content
            "nude", "naked", "nsfw", "explicit", "sexual",
            # Hate speech
            "hate", "racist", "discrimination",
            # Harmful content
            "illegal", "drugs", "abuse",
        ]
        
        # Sensitive keywords that require review
        self.sensitive_keywords = [
            "celebrity", "politician", "public figure",
            "children", "minor", "kid",
        ]
        
        # Allowed exceptions (e.g., artistic contexts)
        self.allowed_contexts = [
            "artistic", "classical art", "renaissance", "sculpture",
            "medical", "educational", "anatomical",
        ]
    
    def is_safe(self, prompt: str) -> bool:
        """
        Check if a prompt is safe to process
        
        Args:
            prompt (str): User prompt to check
            
        Returns:
            bool: True if safe, False if blocked
        """
        prompt_lower = prompt.lower()
        
        # Check for blocked keywords
        for keyword in self.blocked_keywords:
            if keyword in prompt_lower:
                # Check if it's in an allowed context
                has_allowed_context = any(
                    context in prompt_lower for context in self.allowed_contexts
                )
                if not has_allowed_context:
                    return False
        
        return True
    
    def check_prompt(self, prompt: str) -> Tuple[bool, str, List[str]]:
        """
        Comprehensive prompt check with feedback
        
        Args:
            prompt (str): Prompt to check
            
        Returns:
            tuple: (is_safe, message, warnings)
        """
        prompt_lower = prompt.lower()
        warnings = []
        
        # Check blocked keywords
        blocked_found = []
        for keyword in self.blocked_keywords:
            if keyword in prompt_lower:
                # Check for allowed context
                has_allowed_context = any(
                    context in prompt_lower for context in self.allowed_contexts
                )
                if not has_allowed_context:
                    blocked_found.append(keyword)
        
        if blocked_found:
            message = f"Blocked due to inappropriate content: {', '.join(blocked_found)}"
            return False, message, []
        
        # Check sensitive keywords
        sensitive_found = []
        for keyword in self.sensitive_keywords:
            if keyword in prompt_lower:
                sensitive_found.append(keyword)
        
        if sensitive_found:
            warnings.append(
                f"Sensitive content detected: {', '.join(sensitive_found)}. "
                "Please ensure ethical use."
            )
        
        # Check for real people names (basic check)
        if self._might_contain_real_person(prompt):
            warnings.append(
                "This prompt may reference real people. "
                "Please ensure you have appropriate rights and permissions."
            )
        
        # All checks passed
        message = "Prompt passed safety checks"
        if warnings:
            message += " with warnings"
        
        return True, message, warnings
    
    def _might_contain_real_person(self, prompt: str) -> bool:
        """
        Simple check for potential real person references
        
        Args:
            prompt (str): Prompt to check
            
        Returns:
            bool: True if might contain real person reference
        """
        # Check for common patterns
        person_indicators = [
            r'\b(portrait of|photo of|picture of)\s+[A-Z][a-z]+\s+[A-Z][a-z]+',
            r'\b(celebrity|actor|actress|singer|politician)\b',
            r'\b(famous|well-known)\s+(person|figure|individual)\b',
        ]
        
        for pattern in person_indicators:
            if re.search(pattern, prompt, re.IGNORECASE):
                return True
        
        return False
    
    def sanitize_prompt(self, prompt: str) -> str:
        """
        Attempt to sanitize a prompt by removing problematic parts
        
        Args:
            prompt (str): Original prompt
            
        Returns:
            str: Sanitized prompt
        """
        sanitized = prompt
        
        # Remove blocked keywords
        for keyword in self.blocked_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Clean up extra spaces and punctuation
        sanitized = re.sub(r'\s+', ' ', sanitized)
        sanitized = re.sub(r'\s*,\s*,\s*', ', ', sanitized)
        sanitized = sanitized.strip(', ')
        
        return sanitized
    
    def get_filter_report(self, prompt: str) -> dict:
        """
        Generate a detailed filter report
        
        Args:
            prompt (str): Prompt to analyze
            
        Returns:
            dict: Detailed report
        """
        is_safe, message, warnings = self.check_prompt(prompt)
        
        report = {
            "is_safe": is_safe,
            "message": message,
            "warnings": warnings,
            "blocked_keywords_found": [],
            "sensitive_keywords_found": [],
            "sanitized_prompt": self.sanitize_prompt(prompt) if not is_safe else prompt
        }
        
        prompt_lower = prompt.lower()
        
        # Find specific blocked keywords
        for keyword in self.blocked_keywords:
            if keyword in prompt_lower:
                has_allowed_context = any(
                    context in prompt_lower for context in self.allowed_contexts
                )
                if not has_allowed_context:
                    report["blocked_keywords_found"].append(keyword)
        
        # Find specific sensitive keywords
        for keyword in self.sensitive_keywords:
            if keyword in prompt_lower:
                report["sensitive_keywords_found"].append(keyword)
        
        return report


# Ethical guidelines text
ETHICAL_GUIDELINES = """
# Ethical AI Image Generation Guidelines

## Acceptable Use
✅ Creating original artistic works
✅ Generating illustrations for educational content
✅ Designing concepts and prototypes
✅ Personal creative projects
✅ Learning and experimentation

## Prohibited Use
❌ Generating images of real people without consent
❌ Creating misleading or deceptive content
❌ Producing illegal, harmful, or explicit content
❌ Infringing on copyrights or trademarks
❌ Generating content for harassment or discrimination

## Best Practices
1. Always disclose that content is AI-generated
2. Respect intellectual property rights
3. Consider the impact of your generated content
4. Use watermarks to indicate AI origin
5. Don't use AI to replace human creativity without attribution

## Privacy
- Don't generate images depicting identifiable individuals
- Respect privacy rights and personal boundaries
- Be mindful of biases in AI models

## Responsibility
You are responsible for how you use AI-generated content.
Please be ethical, respectful, and mindful of the impact.
"""
