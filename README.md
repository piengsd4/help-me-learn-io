# Help Me Learn IO

AI-powered learning assistant designed to help you achieve your educational goals.

## Tech Stack

- **Frontend:** Vue 3 + TypeScript + Tailwind CSS + Vite
- **Backend:** Django + Django REST Framework
- **Database:** PostgreSQL
- **Task Queue:** Celery + Redis
- **Containerization:** Docker + Docker Compose

## Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 20.19+ or 22.12+ (for local development)
- Python 3.13+ (for local development)

### Using Docker (Recommended)

1. Clone the repository
2. Create `.env` file in the project root (see `.env.example`)
3. Create frontend env files:
   - `hmlio_FE/.env` for local dev, e.g. `VITE_API_URL=http://localhost:8000`
   - `hmlio_FE/.env.production` for Docker/production, e.g. `VITE_API_URL=http://django_app:8000` so the frontend container can reach Django on the compose network
3. Build and start all services:

```bash
docker compose up --build
```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Database: localhost:5432

### Local Development

#### Backend Setup

```bash
cd hmlio_BE
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Frontend Setup

```bash
cd hmlio_FE
npm install
npm run dev
```

## Feature Ideas

**Completed:**
- ~~User inputs a goal + time period~~
- ~~LLM generates a list of todos (instructions)~~
- ~~User can mark each instruction as done~~

**Planned:**
- (Not needed) Whenever an instruction is marked done, it pops up a text telling user to use what they learn for the next instruction
- Need some kind of progression system to keep users engaged
- Notification system when user is not keeping up with schedule
- You can have different goals at the same time (Keeping history as side tabs GPT-style), each goal will be a roadmap of what to do each day (how many days depend on what the user's query is)
- Add an overview page for summary of what to do in each day in case there are several goals

## Steps Before Completion

- ~~Try Async with Celery (Distributed Task Queue) with Redis (or SQS)~~
- Write unit tests, load tests
- Try load balancer (esp. ELB)
- Play around with PostgreSQL
- ~~Complete docker with frontend as well (currently only completed for backend)~~
- Deployment test
