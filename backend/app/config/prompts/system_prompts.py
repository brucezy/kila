alternative_prompts_system_input = """
    You output ONLY valid JSON.
    No explanation. No markdown. No preamble. Just JSON.
    
    Example input: "best laptops"
    Example output:
    {
      "original_prompt": "best laptops",
      "alternatives": [
        {
          "category": "Specific Focus",
          "prompt": "Best laptops for gaming under $1000",
          "reason": "More specific budget and use case"
        },
        {
            "category": "Specific Focus",
            "prompt": "Best laptops for running local AI model",
            "reason": "More specific use case"
      ],
      "total_count": 2
    }
    
    Now handle the user's request:
"""


