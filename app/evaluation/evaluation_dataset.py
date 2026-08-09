EVALUATION_DATA = [

    {
        "question":
        "How do we prevent SQL injection attacks?",


        "answer":
        "SQL injection can be prevented using parameterized queries, input validation and least privilege access.",


        "contexts":[

            "Applications should use prepared statements instead of dynamic SQL.",

            "Database users should follow least privilege principles."

        ],


        "ground_truth":
        "Use parameterized queries and enforce database security controls."

    },


    {

        "question":
        "What is vulnerability severity?",


        "answer":
        "Severity indicates the impact level of a vulnerability.",


        "contexts":[

            "Severity levels include Critical, High, Medium and Low."

        ],


        "ground_truth":
        "Severity represents the risk impact of a security vulnerability."

    }

]