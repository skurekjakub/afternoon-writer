"""Pattern definitions for: academic_register"""

PATTERNS = [
    {
        "name": "academic_geometry",
        "category": "academic_register",
        "regex": r'\bgeometry\s+of\b',
        "cap": 0,
        "description": "Academic register: 'geometry of' [body/situation]",
    },
    {
        "name": "academic_mechanics",
        "category": "academic_register",
        "regex": r'\b(?:the\s+)?mechanics\s+of\b',
        "cap": 0,
        "description": "Academic register: 'mechanics of'",
    },
    {
        "name": "academic_trajectory",
        "category": "academic_register",
        "regex": r'\btrajectory\s+of\b',
        "cap": 0,
        "description": "Academic register: 'trajectory of'",
    },
    {
        "name": "academic_topology",
        "category": "academic_register",
        "regex": r'\btopology\s+of\b',
        "cap": 0,
        "description": "Academic register: 'topology of'",
    },
    {
        "name": "academic_architecture_of",
        "category": "academic_register",
        "regex": r'\barchitecture\s+of\s+(?:shame|grief|fear|the\s+moment|desire|longing|this|that|her|his|their)\b',
        "cap": 0,
        "description": "Academic register: 'architecture of [emotion/abstract]'",
    },
    {
        "name": "academic_choreography_of",
        "category": "academic_register",
        "regex": r'\bchoreography\s+of\b',
        "cap": 0,
        "description": "Academic register: 'choreography of'",
    },
    {
        "name": "academic_dynamics_of",
        "category": "academic_register",
        "regex": r'\b(?:power\s+)?dynamics\s+(?:of|between)\b',
        "cap": 0,
        "description": "Academic register: 'dynamics of/between'",
    },
    {
        "name": "academic_recalibrate",
        "category": "academic_register",
        "regex": r'\brecalibrat(?:ed?|ing|ion)\b',
        "cap": 0,
        "description": "Academic register: recalibrate/recalibration",
    },
    {
        "name": "academic_entropy",
        "category": "academic_register",
        "regex": r'\bentropy\s+of\b',
        "cap": 0,
        "description": "Academic register: 'entropy of'",
    },
    {
        "name": "academic_algorithm",
        "category": "academic_register",
        "regex": r'\balgorithm(?:ic)?\b',
        "cap": 0,
        "description": "Academic register: algorithm/algorithmic in narration",
    },
]

COMBINED_CAP = None
