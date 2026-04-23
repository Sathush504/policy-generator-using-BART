"""Scenario configurations for policy adaptation"""

SCENARIOS = {
    "urban_tech": {
        "name": "Urban Technology Focus",
        "description": "Optimize policy for urban tech-enabled environments with advanced digital infrastructure.",
        "constraints": [
            "High population density requiring scalable solutions",
            "Diverse and multicultural demographics",
            "Complex existing infrastructure and legacy systems",
            "High public expectations for digital services",
            "Limited physical space for infrastructure",
            "Environmental sustainability requirements"
        ],
        "priorities": [
            "Digital transformation and automation",
            "Innovation and technological efficiency",
            "Scalability to serve large populations",
            "Data-driven decision making and analytics",
            "Smart city integration capabilities",
            "Public-private partnerships"
        ],
        "tone": "Professional, innovative, forward-thinking",
        "audience": "Urban administrators, tech companies, digital service providers"
    },
    "rural_accessibility": {
        "name": "Rural Accessibility Focus",
        "description": "Adapt policy for rural areas with limited infrastructure and connectivity challenges.",
        "constraints": [
            "Limited internet connectivity and bandwidth",
            "Scattered population distribution",
            "Lower digital literacy levels",
            "Limited technical support availability",
            "Budget constraints",
            "Geographic barriers"
        ],
        "priorities": [
            "Offline-first solutions and capabilities",
            "Simple, user-friendly interfaces",
            "Community-based service delivery",
            "Mobile-first approach",
            "Digital literacy programs",
            "Cost-effectiveness"
        ],
        "tone": "Simple, accessible, community-oriented",
        "audience": "Rural administrators, community leaders, grassroots organizations"
    },
    "security_focused": {
        "name": "Security & Privacy Focus",
        "description": "Enhanced policy with emphasis on cybersecurity and data protection.",
        "constraints": [
            "Strict regulatory compliance requirements",
            "High-value sensitive data handling",
            "Sophisticated threat landscape",
            "Privacy rights and GDPR-like regulations",
            "Audit and accountability requirements",
            "Cross-border data considerations"
        ],
        "priorities": [
            "End-to-end encryption and security",
            "Multi-factor authentication",
            "Regular security audits and assessments",
            "Data minimization principles",
            "Incident response capabilities",
            "Zero-trust architecture"
        ],
        "tone": "Formal, authoritative, compliance-focused",
        "audience": "Security officers, compliance teams, legal departments"
    },
    "citizen_centric": {
        "name": "Citizen-Centric Services",
        "description": "Policy optimized for maximum citizen engagement and service delivery.",
        "constraints": [
            "Diverse user needs and abilities",
            "Varying levels of digital literacy",
            "Accessibility requirements (disabilities)",
            "Multi-language support needs",
            "24/7 service expectations",
            "Multi-channel delivery requirements"
        ],
        "priorities": [
            "User experience and interface design",
            "Accessibility compliance (WCAG)",
            "Personalized service delivery",
            "Feedback and continuous improvement",
            "Transparency and communication",
            "Response time optimization"
        ],
        "tone": "Friendly, empathetic, service-oriented",
        "audience": "Citizens, service users, advocacy groups"
    },
    "innovation_sandbox": {
        "name": "Innovation & Experimentation",
        "description": "Policy framework enabling rapid innovation and pilot programs.",
        "constraints": [
            "Need for rapid iteration cycles",
            "Uncertainty in outcomes",
            "Risk management requirements",
            "Limited proven solutions",
            "Stakeholder buy-in challenges",
            "Resource allocation flexibility"
        ],
        "priorities": [
            "Agile and iterative development",
            "Proof-of-concept frameworks",
            "Controlled testing environments",
            "Failure tolerance and learning",
            "Cross-functional collaboration",
            "Emerging technology adoption"
        ],
        "tone": "Experimental, flexible, innovation-driven",
        "audience": "Innovation teams, R&D departments, technology partners"
    }
}

def get_scenario_list():
    """Return list of scenario keys and names"""
    return {key: value["name"] for key, value in SCENARIOS.items()}

def get_scenario_details(scenario_key):
    """Get full details for a specific scenario"""
    return SCENARIOS.get(scenario_key, None)