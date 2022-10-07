BIOGRAPHY = """Hey there!
I'm Jason, a Software Engineer on Google's Search Feature Debugger team, helping to design and build world-class debugging and introspection tools for 10s of thousands of Google Search engineers.

I got my BA in Computer Science from New York University, and am Canadian-born, Hong Kong-raised, and American-educated.

Previously to Google, I was an engineer at Squarespace on their Domains team, helping to propose, design, and implement everything required for turning Squarespace into a full-fledged Domain Registrar, building in new features/resiliency layers/observability into the existing Domains and Squarespace Emails product, and creating the first automated Fraud Detection system for Domains at Squarespace.

Before that, I was an engineer on the FPG team at MediaMath, leading a team of three other engineers in building out a mission-critical ETL process as a service from scratch that affected >90% of company revenue. We built out everything from an initial proof of concept to adding in the final layers of resiliency and monitoring. Because of our work, the service directly decreased our client friction by >90%, and enabled multiple new revenue streams for the company.

I'm an all-purpose software engineer with lots of experience in web product engineering, dev-ops automation, and singing in the shower badly.

For web dev, I have prior experience building out APIs/services from scratch in Spring/SpringBoot in Java, Node + Express in JavaScript, or with the Django framework in Python.

For dev-ops, I have setup automated and error-tolerant development pipelines, automated roll-out/deployments, and leveraged framework testing suites in order to increase developer velocity and code-base stability in both professional and personal settings.

Outside of general software development, I have a passion for home bartending and creating small projects. I am an ardent supporter of the EFF and ACLU for their amazing work for netizens and privacy/freedom.

Looking to get in touch? Drop a line at Hello@JasonYao.com.

Let's talk!
"""

SUMMARY_DATA = {
    "address": {
        "address_line_1": "180 Water Street",
        "address_line_2": "Apt. 2217",
        "city": "New York",
        "zone_code": "NY",
        "country_code": "USA",
        "postal_code": "10038",
    },
    "personal_data": {
        "name": "Jason Yao",
        "description": "Jason Yao is a Canadian-born, Hong Kong-raised, and American-educated software engineer currently working at Google in New York. He is an avid supporter of netizen and privacy rights through the EFF, and is a maintainer and contributor of multiple open source projects",
        "image": "https://jasonyao.com/profile.jpg",
        "nationality": "CAN",
        "contact": {
            "email": "Hello@JasonYao.com",
            "phone": "+1 (949) 335-2639",
            "url": "https://www.JasonYao.com",
            "linkedin": "https://www.Linkedin.com/in/JasonYaoNYU",
            "github": "https://Github.com/JasonYao",
        },
    },
    "current_work_summary": {
        "job_title": "Software Engineer",
        "employer": "Google",
        "url": "https://en.wikipedia.org/wiki/Google",
        "type": "Corporation",
        "start_date": "2021-09-27",
    },
    "previous_work_summaries": [
        {
            "job_title": "Software Engineer",
            "employer": "Squarespace",
            "url": "https://en.wikipedia.org/wiki/Squarespace",
            "type": "Corporation",
            "start_date": "2018-03-27",
            "end_date": "2021-09-10",
        },
        {
            "job_title": "Software Engineer",
            "employer": "MediaMath",
            "url": "https://www.linkedin.com/company/mediamath/",
            "type": "Corporation",
            "start_date": "2017-07-03",
            "end_date": "2018-03-23",
        },
    ],
    "education": [
        {
            "type": "University",
            "name": "New York University",
            "url": "https://en.wikipedia.org/wiki/New_York_University",
            "start_date": "2014-09-02",
            "end_date": "2017-05-25",
            "degree": {
                "level": "Bachelors",
                "focus": "Arts",
                "area": "Computer Science",
            },
            "college": "College of Arts & Science",
        },
        {
            "type": "High School",
            "name": "Hong Kong International School",
            "url": "https://en.wikipedia.org/wiki/Hong_Kong_International_School",
            "start_date": "2000-09-05",
            "end_date": "2013-05-25",
        },
    ],
    "skills": {
        "programming": {
            "Languages": [
                "Java",
                "Python",
                "C++",
                "TypeScript",
                "C",
                "Bash",
            ],
            # "Big Data Tools": [
            #     "(Py)Spark + Yarn",
            #     "AWS EMR",
            # ],
            "Web Frameworks": [
                "Spring/SpringBoot",
                "Spring Reactor/WebFlux",
                "Django",
                "Flask",
                "NodeJS",
                "Express",
                "Vue 3",
            ],
            "Data Layer/Caches": [
                "PostgreSQL",
                "MongoDB",
                "Redis",
                "Hibernate",
                "JPA",
                "R2DBC",
            ],
            "Message Buses": [
                "Kafka",
                "AWS SQS",
                "RabbitMQ",
            ],
            "Observability": [
                "Prometheus",
                "Grafana",
                "LightStep",
                "OpenTelemetry",
            ],
            "Tools": [
                "git",
                "vim",
                "Kubernetes",
                "Docker",
                "Github Actions",
                "DroneCD",
                "LaTeX",
                "Consul",
            ]
        },
        "general": {
            "languages": [
                "en",
                "zh"
            ],
            "misc": "I know how to learn, use Google, sing badly in the shower, and read SO"
        }
    }
}

JOB_HISTORY = [
    {
        "company_name": "Google",
        "location": "New York, NY",
        "positions": [
            {
                "title": "Software Engineer L4 (Google Search)",
                "start_date": "2021-09-27",
                "end_date": None,
                "descriptions": [
                    "Proposed, designed, and lead team of 5 SWEs in implementation of a plan to improve Google Search debugging performance, leading to a **99.8% error rate reduction, and ~70% latency improvement**, and over 500 SWE-days saved in time per year",
                    "Proposed, designed, and lead team of 5 SWEs in implementation on next generation service architecture enabling faster developer velocity and additional latency improvements"
                ]
            }
        ]
    },
    {
        "company_name": "Squarespace",
        "location": "New York, NY",
        "positions": [
            {
                "title": "Software Engineer III (Domains)",
                "start_date": "2018-03-27",
                "end_date": "2021-09-10",
                "descriptions": [
                    "First engineer on Domain Registrar team, **turned Squarespace into a Domain Name Registrar**, enabling direct domain registration and management without 3rd parties.",
                    "Designed and built registrar TLS, EPP, and product features that **lowered domain registrations from ~30s to ~100ms (99.6% latency reduction)**",
                    "Designed and built robust backend services and systems for Squarespace Emails that **lowered error rates from ~40% to ~2%**, and **decreased customer support volume from ~60% to <1%**",
                    "Reduced company reliance on 3rd party vendors by building out registrar functionality in-house, lowering domain costs on average by ~20%, and **provided new uptime guarantee of 99.9% compared to old 3rd party's 95% uptime** for all domain actions",
                    "Proposed, designed, and built the backend systems for a generic fraud detection system, increasing the number of identified fraudulently purchased domains by over 3.5 times baseline. Converted fraud detection model at Squarespace from _reactive to customer write-ins_ to _proactively identifying fraudulently purchased domains_",
                    "Wired up deep observability metrics via Prometheus/Graphana, **providing useful technical and business dashboards and alerts in previously opaque systems running in production**"
                ]
            }
        ]
    },
    {
        "company_name": "MediaMath",
        "location": "New York, NY",
        "positions": [
            {
                "title": "Software Engineer I & II",
                "start_date": "2017-07-03",
                "end_date": "2018-03-23",
                "descriptions": [
                    "**Tech Lead** for a company-critical ETL service that **generated all fee data used by thousands of advertising bidders world-wide**",
                    "**Reduced client friction by over 90%**, and unlocked company's potential revenue substantially by enabling individual feature pricing",
                    "**Increased team developer velocity by >300%** (based on story point completions before/after) by creating a command-line API interacting with service subsystems",
                    # "Continued assuming SDE II responsibilities, increasing team cohesion,technical ability, and positive feedback loop implementations",
                    # "Significantly increased visibility and insight into the service by building out monitoring and resiliency layers"
                ]
            }
        ]
    }
]

all_data = {
    "summaries": SUMMARY_DATA,
    "biography": BIOGRAPHY,
    "job_history": JOB_HISTORY,
}
