BIOGRAPHY = """Hey there!
My name is Jason, a Staff Software Engineer and Tech Lead on the Google Search team, leading a 13-engineer team building debugging, distributed tracing, and developer productivity infrastructure for thousands of Search engineer.

I got my BA in Computer Science from New York University, and am Canadian-born, Hong Kong-raised, and American-educated.

Previously to Google, I was an engineer at Squarespace on their Domains team, helping to propose, design, and implement everything required for turning Squarespace into a full-fledged Domain Registrar, building in new features/resiliency layers/observability into the existing Domains and Squarespace Emails product, and creating the first automated fraud detection system for Domains at Squarespace.

I'm an all-purpose software engineer with lots of experience in web product engineering, dev-ops automation, and singing in the shower badly.

Outside of general software development, I have a passion for home bartending and creating small projects. I am an ardent supporter of the EFF and ACLU for their amazing work for netizens and privacy/freedom.

Looking to get in touch? Drop a line at Hello@JasonYao.com.

Let's talk!
"""

SUMMARY_DATA = {
  "address": {
    "city": "New York",
    "zone_code": "NY",
    "country_code": "USA",
  },
  "personal_data": {
    "name": "Jason Yao",
    "description": "Jason Yao is a Canadian-born, Hong Kong-raised, and American-educated Staff Software Engineer and tech lead currently working at Google in New York. He is an avid supporter of netizen and privacy rights through the EFF, and is a maintainer and contributor of multiple open source projects",
    "image": "https://jasonyao.com/profile.jpg",
    "nationality": "CAN",
    "contact": {
      "email": "Hello@JasonYao.com",
      "phone": "+1 (949) 335-2639",
      # Note: urls are case insensitive, but this looks better in title-case
      # on the actual resume itself
      "url": "https://www.JasonYao.com",
      "linkedin": "https://www.Linkedin.com/in/Tea-Gremlin",
      "github": "https://Github.com/JasonYao",
    },
  },
  "current_work_summary": {
    "job_title": "Tech Lead (Search Debug), Staff Software Engineer",
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
        "Kotlin",
        "Java",
        "Python",
        "C++",
        "TypeScript",
        "C",
        "Bash",
      ],
      "AI/ML": [
        "PyTorch",
        "TensorFlow",
        "Diffusers",
        # "Huggingface",
      ],
      # "Big Data Tools": [
      #     "(Py)Spark + Yarn",
      #     "AWS EMR",
      # ],
      "Web Frameworks": [
        "Spring/SpringBoot",
        "Spring Reactor/WebFlux",
        "Django",
        "NodeJS",
        "Vue 3",
        "OpenAPI",
        "Protobuf",
        # "Flask",
        # "Express",
      ],
      "Databases & Processing": [
        "PostgreSQL",
        "MongoDB",
        "Spanner",
        "Redis",
        "Hibernate",
        "JPA",
        "R2DBC",
        "Kafka",
        "AWS SQS",
        # "RabbitMQ",
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
        # "DroneCD",
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
        "title": "Staff Software Engineer",
        "start_date": "2026-11-01",
        "end_date": None,
        "descriptions": [
          "**Tech lead for a 13-engineer team** and cross-org working group lead driving architectural roadmap, trace governance, and reliability across Google Search's debugging and distributed tracing infrastructure",
          "Authored, led, and executed an 8-workstream trace governance and automated culprit-finding architecture, **reducing volume regression diagnosis and rollback from mutli-week incidents to minutes**",
        ]
      },
      {
        "title": "Senior Software Engineer",
        "start_date": "2023-11-01",
        "end_date": "2026-11-01",
        "descriptions": [
          "Spearheaded cross-org distributed tracing stabilization across Search, Evaluations, and Core, **reducing Search trace emissions by 33.1%, cutting p50 latency by 25.7%, and raising eval trace reliability from 15% to 90%**",
          "Productionized an automated protobuf fragmentation and compression pipeline, **reducing emitted debug data volume by 92%**; architected adaptive eval trace sampling for a **64% trace size reduction**",
          "Architected and migrated Search's core debug logging SDK (**11k+ LoC across 100+ PRs**) to introduce team attribution, load shedding, and child context primitives with **zero downstream migration burden**",
          "Designed and led targeted debug data caching, **decreasing latency by 5x, and reducing error rates from 11% to ~0.1%**",
          "Mentored team members, conducted 80+ interviews, and dozens of Hiring Committee reviews",
        ]
      },
      {
        "title": "Software Engineer",
        "start_date": "2021-09-27",
        "end_date": "2023-11-01",
        "descriptions": [
          "Proposed, designed, and led team of 5 SWEs to overhaul Search debugging performance and platform architecture, delivering a **99.8% error rate reduction, ~70% latency improvement**, and **25+ SWE-years saved annually**",
        ]
      }
    ],
    "logos": {
      "short": "logos/short/google",
      "long": "logos/long/google"
    }
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
          # "First engineer on Domain Registrar team, **turned Squarespace into a Domain Name Registrar**, enabling direct domain registration and management without 3rd parties.",
          "Designed and built registrar TLS, EPP, and product features that **lowered domain registrations from ~30s to ~100ms (99.6% latency reduction)**",
          "Designed and built robust backend services and systems for Squarespace Emails that **lowered error rates from ~40% to ~2%**, and **decreased customer support volume from ~60% to <1%**",
          # "Reduced company reliance on 3rd party vendors by building out registrar functionality in-house, lowering domain costs on average by ~20%, and **provided new uptime guarantee of 99.9% compared to old 3rd party's 95% uptime** for all domain actions",
          "Proposed, designed, and built the backend systems for a generic fraud detection system, **increasing the number of correctly-identified fraudulently purchased domains by over 3.5x baseline**. Converted fraud detection model at Squarespace from _reactive to customer write-ins_ to _proactively identifying fraudulently purchased domains_",
          # "Wired up deep observability metrics via Prometheus/Graphana, **providing useful technical and business dashboards and alerts in previously opaque systems running in production**"
        ]
      }
    ],
    "logos": {
      "short": "logos/short/squarespace",
      "long": "logos/long/squarespace"
    }
  }
  # {
  #   "company_name": "MediaMath",
  #   "location": "New York, NY",
  #   "positions": [
  #     {
  #       "title": "Software Engineer I & II",
  #       "start_date": "2017-07-03",
  #       "end_date": "2018-03-23",
  #       "descriptions": [
  #         "**Tech Lead** for a company-critical ETL service that **generated all fee data used by thousands of advertising bidders world-wide**",
  #         "**Reduced client friction by over 90%**, and unlocked company's potential revenue substantially by enabling individual feature pricing",
  #         "**Increased team developer velocity by >300%** (based on story point completions before/after) by creating a command-line API interacting with service subsystems",
  #         "Continued assuming SDE II responsibilities, increasing team cohesion,technical ability, and positive feedback loop implementations",
  #         "Significantly increased visibility and insight into the service by building out monitoring and resiliency layers"
  #       ]
  #     }
  #   ],
  #   "logos": {
  #     "short": "logos/short/mediamath",
  #     "long": "logos/long/mediamath",
  #   }
  # }
]

all_data = {
  "summaries": SUMMARY_DATA,
  "biography": BIOGRAPHY,
  "job_history": JOB_HISTORY,
}
