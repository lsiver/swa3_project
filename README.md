![CI Tests](https://github.com/lsiver/swa3_project/workflows/CI%20Tests/badge.svg)
# swa3_project# - Binary Distillation Column
## https://swa3-project-1.onrender.com
#### An app to simulate binary distillation. Determines the minimum Reflux (Rmin) and minimum theoretical stages (Nmin) for a distillation. As well as the actual stages based on current conditions inputted (each stage being a "flash" calculation). 
#### Uses ideal VLE conditions (Raoult's law xiP* = yiP ~ Ki = yi/xi = P*/P; saturation pressures calculated with antoine's constants). Some plans to expand to using non-ideal factors through Peng-Robinson EOS/VLE...eventually.
#### **Backend**: Python/Flask REST API with Celery for task processing
#### **Frontend** React.js with data visualization components
#### **Infrastructure**: Redis message broker, SQLite database, deployed on Render
#### **Data**: Web-scraped NIST thermodynamic data 