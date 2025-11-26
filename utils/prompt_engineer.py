"""
Prompt Engineering utilities for enhancing text prompts
"""

import random
from utils.config import Config


class PromptEngineer:
    """Class for prompt enhancement and engineering"""
    
    def __init__(self):
        self.config = Config()
    
    def enhance_prompt(self, prompt, style=None):
        """
        Enhance a prompt with quality descriptors
        
        Args:
            prompt (str): Original prompt
            style (str): Optional style to apply
            
        Returns:
            str: Enhanced prompt
        """
        if not prompt.strip():
            return prompt
        
        # Add quality enhancers if not already present
        quality_terms = self.config.QUALITY_ENHANCERS
        
        # Check if prompt already has quality terms
        has_quality = any(term.lower() in prompt.lower() for term in quality_terms)
        
        if not has_quality:
            # Add 2-3 random quality enhancers
            selected_enhancers = random.sample(quality_terms, min(3, len(quality_terms)))
            prompt = f"{prompt}, {', '.join(selected_enhancers)}"
        
        # Add style if specified
        if style and style != "None":
            style_suffix = self.get_style_suffix(style)
            if style_suffix and style_suffix.lower() not in prompt.lower():
                prompt = f"{prompt}, {style_suffix}"
        
        return prompt
    
    @staticmethod
    def get_style_suffix(style):
        """Get style-specific suffix for prompt"""
        config = Config()
        return config.STYLE_PRESETS.get(style, "")
    
    def extract_key_elements(self, prompt):
        """
        Extract key elements from a prompt
        
        Args:
            prompt (str): Input prompt
            
        Returns:
            dict: Dictionary of extracted elements
        """
        elements = {
            "subject": "",
            "style": "",
            "quality": [],
            "lighting": "",
            "composition": ""
        }
        
        # Simple keyword extraction
        prompt_lower = prompt.lower()
        
        # Extract style keywords
        for style_name, style_keywords in self.config.STYLE_PRESETS.items():
            if any(keyword in prompt_lower for keyword in style_keywords.lower().split(", ")):
                elements["style"] = style_name
                break
        
        # Extract quality keywords
        for quality in self.config.QUALITY_ENHANCERS:
            if quality.lower() in prompt_lower:
                elements["quality"].append(quality)
        
        # Extract lighting keywords
        lighting_keywords = ["golden hour", "sunset", "sunrise", "dramatic lighting", 
                            "soft lighting", "neon", "cinematic lighting"]
        for keyword in lighting_keywords:
            if keyword in prompt_lower:
                elements["lighting"] = keyword
                break
        
        # Extract composition keywords
        composition_keywords = ["close-up", "wide angle", "portrait", "landscape", 
                               "aerial view", "bird's eye view"]
        for keyword in composition_keywords:
            if keyword in prompt_lower:
                elements["composition"] = keyword
                break
        
        return elements
    
    def generate_negative_prompt(self, custom_negatives=None):
        """
        Generate a comprehensive negative prompt
        
        Args:
            custom_negatives (list): Additional negative terms
            
        Returns:
            str: Negative prompt
        """
        negatives = self.config.DEFAULT_NEGATIVE_PROMPTS.copy()
        
        if custom_negatives:
            negatives.extend(custom_negatives)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_negatives = []
        for item in negatives:
            if item.lower() not in seen:
                seen.add(item.lower())
                unique_negatives.append(item)
        
        return ", ".join(unique_negatives)
    
    def suggest_improvements(self, prompt):
        """
        Suggest improvements for a prompt
        
        Args:
            prompt (str): Original prompt
            
        Returns:
            list: List of suggestions
        """
        suggestions = []
        prompt_lower = prompt.lower()
        
        # Check for quality descriptors
        if not any(quality.lower() in prompt_lower for quality in self.config.QUALITY_ENHANCERS):
            suggestions.append("Add quality descriptors like 'highly detailed' or '8k resolution'")
        
        # Check for style
        has_style = any(style_keywords.lower() in prompt_lower 
                       for style_keywords in self.config.STYLE_PRESETS.values())
        if not has_style:
            suggestions.append("Specify an art style (e.g., 'photorealistic', 'digital art')")
        
        # Check for lighting
        lighting_keywords = ["lighting", "light", "sunset", "sunrise", "golden hour"]
        if not any(keyword in prompt_lower for keyword in lighting_keywords):
            suggestions.append("Add lighting information for better results")
        
        # Check for composition
        composition_keywords = ["portrait", "landscape", "close-up", "wide angle"]
        if not any(keyword in prompt_lower for keyword in composition_keywords):
            suggestions.append("Specify composition or camera angle")
        
        # Check length
        word_count = len(prompt.split())
        if word_count < 5:
            suggestions.append("Add more descriptive details (current: {word_count} words)")
        elif word_count > 50:
            suggestions.append("Consider simplifying - very long prompts may be less effective")
        
        return suggestions
    
    def analyze_prompt(self, prompt):
        """
        Analyze a prompt and provide detailed feedback
        
        Args:
            prompt (str): Prompt to analyze
            
        Returns:
            dict: Analysis results
        """
        elements = self.extract_key_elements(prompt)
        suggestions = self.suggest_improvements(prompt)
        
        analysis = {
            "original_prompt": prompt,
            "enhanced_prompt": self.enhance_prompt(prompt),
            "elements": elements,
            "suggestions": suggestions,
            "word_count": len(prompt.split()),
            "completeness_score": self._calculate_completeness(prompt)
        }
        
        return analysis
    
    def _calculate_completeness(self, prompt):
        """
        Calculate how complete a prompt is (0-100)
        
        Args:
            prompt (str): Prompt to evaluate
            
        Returns:
            int: Completeness score
        """
        score = 0
        prompt_lower = prompt.lower()
        
        # Has quality terms (20 points)
        if any(quality.lower() in prompt_lower for quality in self.config.QUALITY_ENHANCERS):
            score += 20
        
        # Has style (20 points)
        if any(style.lower() in prompt_lower for style in self.config.STYLE_PRESETS.values()):
            score += 20
        
        # Has adequate length (20 points)
        word_count = len(prompt.split())
        if 10 <= word_count <= 40:
            score += 20
        elif 5 <= word_count < 10:
            score += 10
        
        # Has lighting (20 points)
        lighting_keywords = ["lighting", "light", "sunset", "sunrise", "golden hour", "neon"]
        if any(keyword in prompt_lower for keyword in lighting_keywords):
            score += 20
        
        # Has composition (20 points)
        composition_keywords = ["portrait", "landscape", "close-up", "wide angle", "view"]
        if any(keyword in prompt_lower for keyword in composition_keywords):
            score += 20
        
        return min(score, 100)


# Example prompt templates
EXAMPLE_PROMPTS = {
    "Portrait": "close-up portrait of a person, professional photography, soft lighting, bokeh background, highly detailed, 8k",
    "Landscape": "beautiful mountain landscape at sunset, golden hour lighting, dramatic clouds, highly detailed, professional photography",
    "Fantasy": "fantasy castle on floating island, magical atmosphere, ethereal lighting, fantasy art style, highly detailed",
    "Sci-Fi": "futuristic city with neon lights, cyberpunk style, rain-soaked streets, cinematic lighting, 8k, highly detailed",
    "Animal": "majestic lion portrait, wildlife photography, golden hour lighting, sharp focus, professional, highly detailed",
    "Abstract": "abstract colorful patterns, digital art, vibrant colors, geometric shapes, modern art style, highly detailed",
    "Architecture": "modern architecture building, minimalist design, professional photography, dramatic lighting, 8k resolution",
    "Nature": "enchanted forest with mystical fog, magical atmosphere, fantasy art, highly detailed, professional",
}
