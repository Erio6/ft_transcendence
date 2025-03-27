# ft_transcendence

ft_transcendence is a full-stack web application that enhances the classic Pong game with modern web technologies, security measures, multiplayer capabilities, and advanced graphics. This project integrates multiple cutting-edge features such as Two-Factor Authentication (2FA), AI players, blockchain score storage, and a tournament system.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Security Considerations](#security-considerations)
- [Contributors](#contributors)

## Features
### Authentication & Security
- **Two-Factor Authentication (2FA)** for added security.
- **JSON Web Tokens (JWT)** for secure authentication and authorization.
- **User-friendly setup** for enabling 2FA via SMS, authenticator apps, or email.
- **HashiCorp Vault** for secrets management.
- **Web Application Firewall (WAF) and ModSecurity** for security against attacks.
- **Secure password hashing** and protection against SQL injections/XSS.

### Gameplay Enhancements
- **Multiplayer Mode**: Play against another player in real-time.
- **Tournament System**: Organize and manage tournaments with matchmaking and scheduling.
- **AI Opponent**: A challenging AI that simulates human behavior with strategic gameplay.
- **3D Graphics**: Immersive gameplay experience using **ThreeJS/WebGL**.
- **Server-side Pong Game**: API-driven gameplay, enabling command-line and web interface interactions.

### User Management
- Secure user registration and login.
- Unique display names for tournament participation.
- User profiles with avatars, stats (wins/losses), and match history.
- Friends list with online status.

### Blockchain Integration
- **Ethereum Blockchain** for storing tournament scores securely.
- **Solidity Smart Contracts** for managing and retrieving tournament scores.

### Deployment & Compatibility
- **Single-page application (SPA)** supporting browser navigation (Back/Forward buttons).
- **Dockerized setup** for easy deployment using `docker-compose up `.
- **Rootless Docker Mode** for security.
- **Google Chrome compatibility** with a stable experience.
- **Handling of network issues** for the best user experience in multiplayer mode.

## Technologies Used
- **Frontend**: Vanilla JavaScript
- **Backend**: Django, PostgreSQL, Redis, REST API
- **Graphics**: ThreeJS
- **Security**: HashiCorp Vault, ModSecurity, JWT, WAF
- **Containerization**: Docker
- **Blockchain**: Ethereum, Solidity

## Installation
### Prerequisites
- Docker & Docker Compose installed
- Node.js & npm installed
- Python 3 & Django installed

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Norias1011/ft_transcendence.git
   cd ft_transcendence
   ```
2. Set up environment variables:
   - Create a `.env` file and configure secrets (API keys, database credentials, etc.).
   - Ensure this file is ignored by Git.
3. Start the application:
   ```sh
   docker-compose up
   ```
4. Access the application at `http://localhost:3000`.
5. To delete all the file after running:
   ```
   docker system prune -a -f
   ```

## Usage
- Register and log in securely.
- Enable 2FA for added security.
- Play against another player or AI.
- Join or create a tournament.
- View your match history and tournament stats.
- Add friends and check their online status.
- Participate in blockchain-backed tournament scoring.

## Security Considerations
- **All passwords are hashed before storage.**
- **API keys, credentials, and sensitive data must be stored in HashiCorp Vault.**
- **SQL injections and XSS attacks are mitigated through strict validation.**
- **HTTPS is enforced for secure communication.**
- **Docker runs in rootless mode for additional security.**


Contributions are welcome! Feel free to fork the repo and submit pull requests.

---

Enjoy playing and coding ft_transcendence! 🚀
