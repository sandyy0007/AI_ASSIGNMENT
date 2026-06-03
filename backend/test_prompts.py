"""
Test prompts for AI App Config Compiler
20 test cases: 10 normal + 10 edge cases
"""

NORMAL_PROMPTS = [
    {
        "prompt": "Build an e-commerce platform where customers can browse products, add them to a shopping cart, and checkout with payment processing. The system should support multiple product categories, user reviews, and seller management.",
        "context": "Premium marketplace for digital and physical goods"
    },
    {
        "prompt": "Create a project management tool that allows teams to create projects, manage tasks, assign work to team members, and track progress. Include sprint planning, time tracking, and team collaboration features.",
        "context": "Enterprise project management solution"
    },
    {
        "prompt": "Develop a social networking app where users can create profiles, post updates, follow other users, and engage with content through likes and comments. Include messaging and notification features.",
        "context": "Community-driven social platform"
    },
    {
        "prompt": "Build a CRM system for sales teams to manage customer relationships, track sales opportunities, monitor deals in various stages, and generate sales reports.",
        "context": "Sales enablement platform"
    },
    {
        "prompt": "Create a learning management system for online education where instructors can create courses, students can enroll and complete lessons, take quizzes, and track progress with certificates.",
        "context": "Online education platform"
    },
    {
        "prompt": "Develop a health and fitness app where users can track workouts, log nutrition, set fitness goals, and view progress with analytics dashboards.",
        "context": "Personal health and wellness tracking"
    },
    {
        "prompt": "Build a content management system for publishing blogs and articles with features for drafting, scheduling, publishing, and analytics.",
        "context": "Digital publishing platform"
    },
    {
        "prompt": "Create a booking system for appointment scheduling with calendar integration, automated reminders, and customer notifications for services like doctors, salons, and consultants.",
        "context": "Service appointment platform"
    },
    {
        "prompt": "Develop an inventory management system for retail businesses to track stock, manage suppliers, handle orders, and generate inventory reports.",
        "context": "Retail inventory solution"
    },
    {
        "prompt": "Build a video streaming platform where users can upload, watch, comment on videos with features for playlists, subscriptions, and recommendations.",
        "context": "User-generated content platform"
    }
]

EDGE_CASE_PROMPTS = [
    {
        "prompt": "Create an ultra-low latency real-time collaborative editing tool for multiple users to edit documents simultaneously with instant synchronization and conflict resolution.",
        "context": "Complex distributed system requirement"
    },
    {
        "prompt": "Build a system with minimal requirements - just 'an app'",
        "context": "Vague requirement"
    },
    {
        "prompt": "Develop an AI-powered recommendation engine that uses machine learning to predict user preferences, powered by complex algorithms and neural networks processing petabytes of data in real-time across distributed infrastructure.",
        "context": "Complex ML system"
    },
    {
        "prompt": "Create a simple counter app that increments a number when you click a button.",
        "context": "Oversimplified requirement"
    },
    {
        "prompt": "Build a hyperscale social network similar to Facebook but supporting 2 billion concurrent users with guaranteed 99.9999% uptime SLA, sub-millisecond latency, and full end-to-end encryption.",
        "context": "Extreme scalability requirement"
    },
    {
        "prompt": "Develop a regulatory compliance system that handles GDPR, HIPAA, CCPA, and 50 other international regulations simultaneously with automated audit trails and legal documentation.",
        "context": "Highly regulated system"
    },
    {
        "prompt": "Create an offline-first mobile app that works perfectly without any internet connection, syncs when connection is available, handles conflicts, and works across 10 different mobile platforms.",
        "context": "Complex sync requirement"
    },
    {
        "prompt": "Build a IoT platform connecting 1 million edge devices sending data continuously with real-time processing, anomaly detection, and 0% data loss.",
        "context": "Massive scale IoT"
    },
    {
        "prompt": "Develop a blockchain-based decentralized social network with smart contracts, cryptocurrency integration, NFT support, and Web3 authentication.",
        "context": "Emerging tech stack"
    },
    {
        "prompt": "Create an app for managing tasks with conflicting requirements: it must be super simple but also have every enterprise feature possible, free but requiring premium subscriptions, fast but processing complex AI algorithms.",
        "context": "Contradictory requirements"
    }
]

TEST_PROMPTS = NORMAL_PROMPTS + EDGE_CASE_PROMPTS
