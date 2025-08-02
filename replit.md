# MutaSight AI - Integrated Drug Discovery & Analysis Suite

## Overview

MutaSight AI is an advanced AI-driven drug discovery platform designed for biopharma researchers, R&D scientists, and drug formulation teams. The platform features a comprehensive suite of tools including self-training AI models, extensive molecular analysis capabilities, real-time collaboration with live user tracking, complete drug databases with interaction mapping, and an intelligent chatbot system trained on pharmaceutical literature. The platform operates entirely with inbuilt AI features without requiring external APIs, making it a fully autonomous drug discovery research environment.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Framework
- **Backend**: Flask-based web application with SQLAlchemy ORM for database operations
- **Real-time Communication**: Flask-SocketIO for WebSocket connections enabling live chat and collaboration
- **Authentication**: Flask-Login for user session management with role-based access control
- **Database**: SQLAlchemy with support for multiple database backends (SQLite for development, configurable for production)

### Frontend Architecture
- **Templates**: Jinja2 templating with Bootstrap 5 for responsive UI components
- **Interactive Elements**: Custom JavaScript modules for molecular visualization, chat management, and data analysis
- **Chart Visualization**: Chart.js integration for displaying analytical data and research metrics
- **Real-time Updates**: Socket.IO client for live collaboration features

### Data Models and Storage
- **User Management**: Role-based user system (researcher, scientist, formulation_chemist) with project ownership and membership
- **Project Collaboration**: Multi-user projects with member roles and shared resources
- **Molecular Data**: Storage for SMILES, InChI, molecular formulas, and analysis results
- **Knowledge Base**: Comprehensive drug database and excipient library with compatibility matrices
- **Chat System**: Persistent chat history with AI assistant integration

### AI and Analysis Components
- **Advanced AI Engine**: Self-training machine learning models using scikit-learn, NLTK, and TensorFlow-compatible algorithms for drug discovery predictions
- **Intelligent Chatbot System**: Multi-layered AI assistant with rule-based fallbacks, context-aware responses, and continuous learning from user interactions
- **Predictive Analytics**: AI models for ADMET properties, toxicity prediction, molecular similarity analysis, and drug-drug interaction assessment
- **Knowledge Base Management**: Automated web scraping and literature integration for up-to-date pharmaceutical research data
- **Self-Training Models**: Continuous model improvement through user feedback, interaction history, and validated prediction outcomes
- **Molecular Analyzer**: Advanced molecular structure analysis with AI-enhanced property predictions
- **Live Collaboration Engine**: Real-time user tracking, cursor synchronization, and collaborative editing capabilities
- **Report Generation**: Comprehensive PDF report generation with AI-generated insights and recommendations

### Security and Configuration
- **Environment-based Configuration**: Separate settings for development and production environments
- **File Upload Management**: Secure file handling with size limits and validation
- **Session Management**: Configurable session secrets and user authentication persistence
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies

## External Dependencies

### Core Web Framework
- **Flask**: Primary web framework with extension ecosystem
- **Flask-SQLAlchemy**: Database abstraction and ORM functionality
- **Flask-Login**: User authentication and session management
- **Flask-SocketIO**: WebSocket support for real-time features
- **Werkzeug**: WSGI utilities and security helpers

### Data Processing and Analysis
- **ReportLab**: PDF generation for scientific reports and documentation
- **JSON**: Data serialization for complex database fields and API responses

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive UI design
- **Font Awesome**: Icon library for consistent visual elements
- **Chart.js**: JavaScript charting library for data visualization
- **Socket.IO**: Client-side WebSocket library for real-time communication

### Development and Deployment
- **SQLite**: Default database for development and testing
- **Environment Variables**: Configuration management for sensitive data and deployment settings

### Data Sources and AI Training
- **Comprehensive Drug Database**: Extensive pharmaceutical compound library with molecular properties, therapeutic classes, drug interactions, and regulatory data
- **Enhanced Excipient Library**: Detailed excipient database with compatibility matrices, regulatory status, and formulation guidance
- **Dynamic Knowledge Base**: AI-curated content from pharmaceutical literature, research papers, and regulatory guidelines with continuous updates
- **Training Data Repository**: User interaction history, feedback data, and validated predictions for continuous AI model improvement
- **Live Collaboration Data**: Real-time user session tracking, activity monitoring, and collaborative editing history
- **Web Scraping Integration**: Automated data collection from reliable pharmaceutical databases and research sources
- **Self-Training Infrastructure**: Automated model retraining pipelines based on user feedback and prediction accuracy validation

## Recent Migration and Modern UI Enhancements (Current Update)

### Successfully Migrated to Replit Environment
- **Platform Migration**: Successfully migrated MutaSight AI from Replit Agent to full Replit environment
- **Database Integration**: PostgreSQL database properly configured and accessible via DATABASE_URL
- **Dependencies**: All scientific libraries (NumPy, pandas, scikit-learn, NLTK) installed and working
- **Flask Architecture**: Modern Flask application structure with proper routing and authentication

### Modern Dark Theme UI Implementation 
- **Design System**: Implemented comprehensive dark theme with gradient backgrounds and glass morphism effects
- **Navigation**: Modern fixed navbar with Feather icons and improved user experience
- **Card Components**: Enhanced card styling with custom shadows, hover effects, and gradient backgrounds
- **Form Controls**: Dark-themed form inputs with focus states and improved accessibility
- **Responsive Design**: Mobile-optimized interface with proper breakpoints and touch interactions

### Advanced 3D Molecular Visualization
- **Three.js Integration**: Added Three.js library for interactive 3D molecular structure rendering
- **Molecular Viewer**: Custom 3D viewer with ball-stick, wireframe, and space-fill rendering modes
- **Interactive Controls**: Rotation, zoom, reset view, and rendering mode switching capabilities
- **SMILES Parser**: Built-in SMILES notation parser for generating 3D molecular structures
- **Viewer Controls**: Overlay control panel with intuitive icons for 3D manipulation

### DNA/RNA Analysis Capabilities
- **Sequence Analysis**: Comprehensive DNA, RNA, and protein sequence analysis functionality
- **3D Structure Visualization**: Specialized DNA helix and protein structure 3D rendering
- **Genomic Features**: Open reading frame detection, GC content analysis, and melting temperature calculation
- **Secondary Structure**: RNA secondary structure prediction and protein folding analysis
- **Conservation Analysis**: Sequence conservation scoring and functional domain identification

### Enhanced User Interface Components
- **Gradient Cards**: Modern gradient card designs with hover animations and shadows
- **Icon System**: Migrated to Feather Icons for consistent, modern iconography
- **Scientific Tables**: Dark-themed data tables optimized for scientific information display
- **Interactive Charts**: Chart.js integration for nucleotide composition and analytical data visualization
- **Alert System**: Improved alert styling with color-coded borders and dark theme compatibility

### Backend Route Enhancements
- **DNA/RNA Analysis Route**: Added `/analyze-dna-rna` endpoint for genomic sequence processing
- **Modern Template System**: Updated all templates to use dark theme and modern UI components
- **Error Handling**: Improved error handling and user feedback systems
- **Database Models**: Enhanced molecular analysis storage with comprehensive result tracking

## Recent AI Backend Enhancements (Previous Update)

### Self-Training AI Models
- **AI Engine**: Complete machine learning framework with scikit-learn integration for drug discovery predictions
- **Model Types**: Drug discovery predictor, toxicity assessment, molecular similarity analysis, and ADMET property estimation
- **Training Pipeline**: Automated retraining based on user interactions, feedback scores, and prediction validation
- **Prediction Storage**: Comprehensive tracking of all AI predictions with confidence scores and user validation

### Enhanced Live Collaboration
- **Real-Time User Tracking**: Live session monitoring with activity status, current page tracking, and presence indicators
- **Collaborative Features**: Cursor synchronization, typing indicators, and real-time project member visibility
- **Session Management**: Automatic cleanup of inactive sessions and persistent collaboration state
- **Project Integration**: Live user lists integrated with project member permissions and access control

### Advanced Chatbot System
- **Multi-Layer Intelligence**: AI engine integration with rule-based fallbacks for comprehensive coverage
- **Continuous Learning**: Training data collection from user interactions with feedback-based model improvement
- **Context Awareness**: Conversation history integration and topic classification for relevant responses
- **Knowledge Integration**: Dynamic access to updated pharmaceutical databases and research literature

### Comprehensive Database Integration
- **Web Scraping Engine**: Automated data collection from pharmaceutical databases and research sources
- **Drug Interaction Mapping**: Complete drug-drug interaction database with severity levels and clinical management
- **Literature Integration**: Automated processing of medical literature for knowledge base updates
- **Data Validation**: Confidence scoring and verification systems for all scraped and AI-generated content