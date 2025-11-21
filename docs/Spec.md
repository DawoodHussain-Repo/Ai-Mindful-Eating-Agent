# Mindful Eating Agent - Technical Architecture Document

**Project**: Mindful Eating Agent Development  
**Document Version**: 1.0  
**Date**: November 2025  
**Authors**: Gulsher Khan (Tech Lead), Ahsan Faraz (AI/ML Developer),Dawood Hussain Project Manager 

---

## 1. Executive Summary

The Mindful Eating Agent is an AI-powered mobile application that provides automated food recognition, nutritional analysis, and personalized dietary recommendations. The system employs custom-trained deep learning models without external LLM APIs, ensuring data privacy and offline capability.

---

## 2. Technology Stack Overview

### 2.1 Web Application Layer
- **Frontend Framework**: HTML5, CSS3, JavaScript
- **Backend Framework**: Flask (Python 3.10)
- **UI Framework**: Custom CSS with responsive design
- **Form Handling**: HTML Forms with Flask-WTF
- **Local Storage**: Browser LocalStorage
- **Session Management**: Flask-Session

### 2.2 Backend Services Layer
- **Runtime**: Python 3.10
- **Framework**: Flask 3.x
- **API Architecture**: RESTful API with session-based authentication
- **Database**: SQLite (development), PostgreSQL (production)
- **Caching**: Flask-Caching
- **Template Engine**: Jinja2

### 2.3 AI/ML Infrastructure
- **Primary Framework**: TensorFlow 2.14 (Python 3.10)
- **Computer Vision**: OpenCV 4.8
- **Model Training**: TensorFlow/Keras API
- **Model Serving**: TensorFlow Serving 2.14
- **Data Processing**: NumPy, Pandas, Scikit-learn
- **Image Augmentation**: Albumentations

### 2.4 Cloud Infrastructure
- **Cloud Provider**: AWS
- **Compute**: EC2 (t3.medium for API, g4dn.xlarge for ML inference)
- **Storage**: S3 (model artifacts, images), EBS (databases)
- **CDN**: CloudFront
- **Load Balancing**: Application Load Balancer (ALB)
- **Monitoring**: CloudWatch

### 2.5 DevOps & Tools
- **Version Control**: Git, GitHub
- **CI/CD**: GitHub Actions
- **Containerization**: Docker 24.x
- **Orchestration**: Docker Compose (development)
- **Testing**: Jest (unit), Detox (E2E), pytest (ML models)
- **Code Quality**: ESLint, Prettier, SonarQube

---

## 3. AI Agent Architecture

### 3.1 Agent Design Philosophy
The Mindful Eating Agent operates as a **semi-autonomous intelligent assistant** with four core cognitive capabilities:

1. **Perception**: Visual understanding through computer vision
2. **Reasoning**: Nutritional analysis and goal assessment
3. **Learning**: Continuous improvement from user interactions
4. **Action**: Proactive recommendations and notifications

### 3.2 Agent Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  AGENT INTERFACE LAYER                  │
│              (Web App User Interface)                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   PERCEPTION MODULE                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Text Input   │  │ Food         │  │ Portion Size │  │
│  │ & Parse      │→ │ Recognition  │→ │ Estimation   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    KNOWLEDGE BASE                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Nutritional  │  │ User Profile │  │ Behavioral   │  │
│  │ Database     │  │ & Preferences│  │ Rules        │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   REASONING ENGINE                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Nutritional  │  │ Pattern      │  │ Goal         │  │
│  │ Analysis     │→ │ Recognition  │→ │ Alignment    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    LEARNING MODULE                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Preference   │  │ Model        │  │ Reinforcement│  │
│  │ Learning     │  │ Fine-tuning  │  │ Learning     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                     ACTION MODULE                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Logging &    │  │ Personalized │  │ Behavioral   │  │
│  │ Tracking     │  │ Recommender  │  │ Nudging      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 3.3 Agent Autonomy Levels
- **Level 1 (Manual)**: User initiates food logging, agent processes
- **Level 2 (Assisted)**: Agent suggests actions based on context
- **Level 3 (Autonomous)**: Agent proactively notifies and recommends
- **Level 4 (Supervised)**: All autonomous actions reviewed by user

---

## 4. Machine Learning Models

### 4.1 Food Recognition Model

**Architecture**: Custom Convolutional Neural Network (CNN)

**Base Architecture**: EfficientNetV2-M (modified)
- Input: 224x224x3 RGB images
- Backbone: EfficientNetV2-M (pre-trained on ImageNet, fine-tuned)
- Custom classifier head: 1000+ food classes
- Output: Food class probabilities + confidence scores

**Training Dataset**:
- Primary: Food-101 dataset (101,000 images, 101 classes)
- Supplementary: UECFOOD-256 dataset (31,395 images, 256 classes)
- Custom collected: 15,000 images (regional foods)
- Total: ~147,000 training images

**Data Augmentation**:
- Random rotation (±15°)
- Random brightness/contrast (±20%)
- Random zoom (0.8-1.2x)
- Horizontal flip
- Color jittering
- Cutout/Random erasing

**Training Configuration**:
- Loss: Categorical cross-entropy
- Optimizer: Adam (lr=0.001, decay)
- Batch size: 32
- Epochs: 100 (early stopping with patience=10)
- Hardware: NVIDIA Tesla T4 GPU
- Training time: ~48 hours

**Performance Metrics**:
- Top-1 Accuracy: 95.2% (target: ≥95%)
- Top-5 Accuracy: 98.7%
- Average inference time: 0.3 seconds (mobile)
- Model size: 52 MB (quantized for mobile)

### 4.2 Portion Size Estimation Model

**Architecture**: Multi-task CNN with depth estimation

**Approach**: Reference object detection + depth estimation
- Input: Food image + optional reference (phone, hand, coin)
- Method: Semantic segmentation + pixel-to-volume mapping
- Output: Portion size in grams/milliliters

**Training**:
- Dataset: Custom annotated dataset (8,000 images with weights)
- Transfer learning from food recognition model
- Fine-tuned for 30 epochs
- Accuracy: ±15% error margin

### 4.3 Recommendation Engine

**Architecture**: Hybrid collaborative-content filtering

**Components**:
1. **Content-based filtering**: Nutritional similarity matching
2. **Collaborative filtering**: Matrix factorization (SVD++)
3. **Context-aware**: Time, location, meal type
4. **Reinforcement learning**: User feedback optimization

**Training**:
- User interaction logs (clicks, ratings, consumption)
- Periodic batch training (weekly)
- Online learning for personalization

**Algorithm**:
```
Recommendation_Score = α × Content_Similarity + 
                       β × Collaborative_Score + 
                       γ × Context_Relevance + 
                       δ × RL_Policy_Value
```

---

## 5. System Architecture

### 5.1 High-Level Architecture

```
Mobile App (iOS/Android)
    ↓ HTTPS/REST
API Gateway (Express.js)
    ↓
┌──────────────┬──────────────┬──────────────┐
│ Auth Service │ Food Service │ User Service │
└──────────────┴──────────────┴──────────────┘
    ↓               ↓               ↓
┌──────────────┬──────────────┬──────────────┐
│ PostgreSQL   │ ML Inference │ MongoDB      │
│ (User/Auth)  │ Service      │ (Logs)       │
└──────────────┴──────────────┴──────────────┘
    ↓               ↓               ↓
┌──────────────┬──────────────┬──────────────┐
│ Redis Cache  │ RabbitMQ     │ S3 Storage   │
└──────────────┴──────────────┴──────────────┘
```

### 5.2 Mobile Application Architecture

**Layer Structure**:
1. **Presentation Layer**: React Native components
2. **Business Logic Layer**: Redux stores, middleware
3. **Data Access Layer**: API clients, local storage
4. **Native Module Layer**: Camera, sensors, notifications

**Offline Capabilities**:
- Local SQLite database for recent meals
- Cached nutritional data (top 500 foods)
- Queued sync for offline entries
- Basic recommendation engine (rule-based fallback)

### 5.3 Backend Service Architecture

**Microservice Components**:

1. **Authentication Service**
   - JWT token generation/validation
   - OAuth 2.0 integration (Google, Apple)
   - Biometric authentication support

2. **Food Recognition Service**
   - Image preprocessing pipeline
   - ML model inference
   - Result caching (Redis)
   - Confidence threshold filtering

3. **Nutritional Analysis Service**
   - Nutrient calculation
   - USDA database integration
   - Macro/micronutrient tracking
   - Daily goal comparison

4. **Recommendation Service**
   - Personalized meal suggestions
   - Alternative food recommendations
   - Recipe matching
   - Context-aware filtering

5. **User Profile Service**
   - Preference management
   - Goal tracking
   - Progress analytics
   - Achievement system

6. **Notification Service**
   - Push notification scheduling
   - Behavioral nudging logic
   - Time-based reminders
   - Achievement notifications

### 5.4 Data Architecture

**PostgreSQL Schema**:
```
users (id, email, password_hash, created_at, updated_at)
user_profiles (user_id, age, gender, height, weight, activity_level, dietary_preferences)
food_logs (id, user_id, food_id, timestamp, portion_size, meal_type)
foods (id, name, category, calories, protein, carbs, fat, fiber, vitamins)
goals (user_id, goal_type, target_value, start_date, end_date)
achievements (user_id, badge_type, earned_at)
```

**MongoDB Collections**:
```
user_interactions (user_id, action_type, context, timestamp)
recommendation_feedback (user_id, recommendation_id, rating, timestamp)
system_logs (service, level, message, timestamp)
analytics_events (user_id, event_type, properties, timestamp)
```

---

## 6. AI Model Training Pipeline

### 6.1 Data Collection & Preparation

**Phase 1: Data Acquisition**
- Public datasets: Food-101, UECFOOD-256, Recipe1M
- Custom photography: Team-collected regional foods
- User-contributed: Anonymous crowdsourced images
- Total dataset: 150,000+ images

**Phase 2: Data Cleaning**
- Duplicate removal
- Quality filtering (blur detection, resolution check)
- Invalid image removal
- Labeling verification (manual + automated)

**Phase 3: Data Annotation**
- Bounding box annotation (portion estimation)
- Multi-label classification (mixed dishes)
- Metadata tagging (meal type, cuisine)
- Quality assurance review

**Phase 4: Data Splitting**
- Training set: 70% (105,000 images)
- Validation set: 15% (22,500 images)
- Test set: 15% (22,500 images)
- Stratified sampling by class

### 6.2 Model Training Process

**Environment Setup**:
```
Hardware: NVIDIA Tesla T4 GPU (16GB VRAM)
OS: Ubuntu 22.04 LTS
Python: 3.10.12
TensorFlow: 2.14.0
CUDA: 11.8
cuDNN: 8.6
```

**Training Pipeline**:
1. Data loading with tf.data.Dataset (prefetching, parallel loading)
2. On-the-fly augmentation
3. Mixed precision training (FP16)
4. Learning rate scheduling (ReduceLROnPlateau)
5. Model checkpointing (best validation accuracy)
6. TensorBoard logging

**Hyperparameter Tuning**:
- Grid search for learning rate, batch size, dropout
- Bayesian optimization for architecture parameters
- Cross-validation for generalization assessment

### 6.3 Model Evaluation & Validation

**Metrics**:
- Accuracy, Precision, Recall, F1-Score
- Confusion matrix analysis
- Per-class performance
- Inference latency profiling
- Model size assessment

**Validation Tests**:
- Cross-dataset validation (test on unseen datasets)
- Adversarial robustness testing
- Edge case evaluation (poor lighting, angles)
- Real-world user testing (100+ participants)

### 6.4 Model Optimization

**Techniques Applied**:
1. **Quantization**: INT8 quantization (52MB → 13MB)
2. **Pruning**: 20% weight pruning (minimal accuracy loss)
3. **Knowledge Distillation**: Teacher-student training
4. **TensorFlow Lite conversion**: Mobile optimization

**Mobile Optimization**:
- TFLite model: 13 MB
- On-device inference: <300ms
- Battery consumption: <2% per 100 inferences

---

## 7. Security & Privacy

### 7.1 Data Security

**Encryption**:
- Data at rest: AES-256 encryption (database, S3)
- Data in transit: TLS 1.3
- API authentication: JWT with RS256 signing
- Password hashing: bcrypt (cost factor 12)

**Access Control**:
- Role-based access control (RBAC)
- Principle of least privilege
- API rate limiting (100 req/min per user)
- IP whitelisting for admin endpoints

### 7.2 Privacy Protection

**Data Handling**:
- GDPR compliance (right to deletion, data portability)
- Data minimization (collect only necessary data)
- Anonymization for analytics
- User consent management

**AI Model Privacy**:
- Federated learning approach (future enhancement)
- Local model caching (sensitive data doesn't leave device)
- No user images stored on servers (processed and discarded)
- Differential privacy in aggregate statistics

---

## 8. Performance Optimization

### 8.1 Mobile App Optimization

**Techniques**:
- Code splitting and lazy loading
- Image optimization (WebP format, lazy loading)
- Memoization of expensive computations
- Virtual lists for large datasets
- Background processing for ML inference

**Performance Targets**:
- App launch time: <2 seconds
- Food recognition: <3 seconds end-to-end
- Screen transition: <100ms
- Memory usage: <150MB
- Battery impact: Minimal (background optimization)

### 8.2 Backend Optimization

**Caching Strategy**:
- Redis for frequently accessed data (nutritional info)
- API response caching (CDN level)
- Database query result caching
- ML inference result caching (image hash based)

**Database Optimization**:
- Indexing on frequently queried fields
- Query optimization (EXPLAIN analysis)
- Connection pooling
- Read replicas for scaling

**Load Balancing**:
- Round-robin distribution
- Health checks every 30 seconds
- Auto-scaling based on CPU (>70% trigger)

---

## 9. Deployment Architecture

### 9.1 Mobile App Deployment

**iOS**:
- TestFlight for beta testing
- App Store distribution
- Minimum version: iOS 14.0
- Target devices: iPhone 8 and newer

**Android**:
- Google Play Console for beta testing
- Play Store distribution
- Minimum version: Android 10.0 (API 29)
- Target devices: Mid-range and flagship

### 9.2 Backend Deployment

**Infrastructure**:
```
┌─────────────────────────────────────────────────┐
│            CloudFront CDN (Global)              │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│       Application Load Balancer (AWS ALB)       │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│       EC2 Auto Scaling Group (2-6 instances)    │
│              t3.medium instances                │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│   RDS PostgreSQL (Multi-AZ) + MongoDB Atlas    │
│   ElastiCache Redis + S3 Storage                │
└─────────────────────────────────────────────────┘
```

**ML Inference Deployment**:
- Dedicated EC2 g4dn.xlarge (GPU instance)
- TensorFlow Serving container
- Model versioning support
- A/B testing capability

**CI/CD Pipeline**:
1. Code push to GitHub
2. GitHub Actions trigger
3. Automated testing (unit, integration)
4. Docker image build
5. Push to ECR
6. Deploy to staging
7. Automated smoke tests
8. Manual approval
9. Blue-green deployment to production

---

## 10. Monitoring & Observability

### 10.1 Application Monitoring

**Metrics Tracked**:
- Request latency (p50, p95, p99)
- Error rates (4xx, 5xx)
- API throughput (requests/second)
- ML inference time
- Database query performance
- Cache hit rates

**Tools**:
- CloudWatch for infrastructure metrics
- Custom logging with Winston (Node.js)
- Sentry for error tracking
- CloudWatch Logs for centralized logging

### 10.2 ML Model Monitoring

**Metrics**:
- Prediction confidence distribution
- Inference latency trends
- Model accuracy drift detection
- User feedback scores
- Edge case frequency

**Alerting**:
- Model accuracy below 93% → retrain
- Inference time > 5 seconds → scale up
- Error rate > 5% → investigate

---

## 11. Testing Strategy

### 11.1 Mobile App Testing

**Unit Testing**:
- Jest for JavaScript/TypeScript
- Coverage target: >80%
- Component testing with React Testing Library

**Integration Testing**:
- API integration tests
- Navigation flow tests
- State management tests

**E2E Testing**:
- Detox for end-to-end scenarios
- Critical user journey coverage
- Automated regression testing

### 11.2 Backend Testing

**Unit Testing**:
- Mocha/Chai for Node.js
- pytest for Python ML services
- Coverage target: >85%

**API Testing**:
- Postman/Newman for API tests
- Load testing with Apache JMeter
- Security testing with OWASP ZAP

### 11.3 ML Model Testing

**Testing Approach**:
- Cross-validation (5-fold)
- Hold-out test set evaluation
- Real-world user testing (UAT)
- Edge case testing (100+ scenarios)
- A/B testing in production

---

## 12. Scalability Considerations

### 12.1 Horizontal Scaling

**Application Layer**:
- Stateless API design
- Session management in Redis
- Auto-scaling based on metrics
- Load balancer distribution

**Database Layer**:
- Read replicas for scaling reads
- Sharding strategy for large datasets
- Connection pooling optimization

### 12.2 Vertical Scaling

**ML Inference**:
- GPU instance scaling (g4dn.xlarge → g4dn.4xlarge)
- Batch inference for efficiency
- Model parallelism for large models

---

## 13. Future Enhancements

### 13.1 Planned Features

1. **Voice Assistant Integration**
   - Voice-based food logging
   - Conversational recommendations

2. **Federated Learning**
   - Privacy-preserving model training
   - On-device personalization

3. **AR Integration**
   - AR-based portion size estimation
   - Virtual meal planning

4. **IoT Integration**
   - Smart scale integration
   - Fitness tracker synchronization

### 13.2 Technology Roadmap

**Q1 2026**: Model v2.0 with improved accuracy (97%+)
**Q2 2026**: Federated learning implementation
**Q3 2026**: Multi-language support (Spanish, French, Urdu)
**Q4 2026**: AR features and wearable integration

---

## 14. Appendices

### 14.1 Key Dependencies

**Mobile App**:
- react-native: 0.72.x
- redux: 4.2.x
- react-native-camera: 4.x
- axios: 1.5.x
- AsyncStorage: 1.19.x

**Backend**:
- express: 4.18.x
- jsonwebtoken: 9.x
- bcrypt: 5.x
- pg (PostgreSQL): 8.11.x
- mongoose: 7.x

**ML/AI**:
- tensorflow: 2.14.x
- opencv-python: 4.8.x
- numpy: 1.24.x
- pandas: 2.0.x
- scikit-learn: 1.3.x

### 14.2 Model Artifacts

**Food Recognition Model**:
- File: `food_recognition_v1.0.tflite`
- Size: 13 MB (quantized)
- Input shape: [1, 224, 224, 3]
- Output shape: [1, 1024] (class probabilities)

**Portion Estimation Model**:
- File: `portion_estimation_v1.0.tflite`
- Size: 8 MB
- Input shape: [1, 224, 224, 3]
- Output: scalar (grams)

---

**Document Control**:
- Version: 1.0
- Last Updated: November 2025
- Next Review: December 2025
- Owner: Technical Team

**Approval**:
- Technical Lead: Gulsher Khan
- AI/ML Developer: Ahsan Faraz
- Project Manager: Dawood Hussain