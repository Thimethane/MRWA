# MRWA Android Application

## Overview

The MRWA Android app delivers a native, material design experience for autonomous AI workflow execution on Android devices. Built with Kotlin, Jetpack Compose, and modern Android architecture components, it provides offline capabilities, real-time synchronization, and seamless MRWA Core integration.

## Features

- ✅ **Material You Design** - Dynamic theming following Material Design 3
- ✅ **Jetpack Compose UI** - Modern, declarative UI framework
- ✅ **Offline-First** - Execute workflows without internet connectivity
- ✅ **Real-Time Sync** - WebSocket-based state synchronization
- ✅ **File Management** - Import from storage, Drive, and other apps
- ✅ **Background Execution** - WorkManager for reliable task execution
- ✅ **Notifications** - Workflow status updates and completion alerts
- ✅ **Dark Theme** - System-wide dark mode support
- ✅ **Multi-Device Sync** - Synchronized across phones and tablets

## Project Structure

```
platforms/android/
├── README.md                        # This file
├── app/
│   ├── build.gradle.kts             # App-level Gradle config
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/mrwa/
│   │   │   │   ├── MRWAApplication.kt
│   │   │   │   ├── ui/
│   │   │   │   │   ├── workflow/
│   │   │   │   │   │   ├── WorkflowListScreen.kt
│   │   │   │   │   │   ├── WorkflowDetailScreen.kt
│   │   │   │   │   │   └── ExecutionLogScreen.kt
│   │   │   │   │   ├── components/
│   │   │   │   │   │   ├── StatusCard.kt
│   │   │   │   │   │   ├── TaskList.kt
│   │   │   │   │   │   └── ArtifactCard.kt
│   │   │   │   │   └── theme/
│   │   │   │   │       ├── Color.kt
│   │   │   │   │       ├── Theme.kt
│   │   │   │   │       └── Type.kt
│   │   │   │   ├── viewmodel/
│   │   │   │   │   ├── WorkflowViewModel.kt
│   │   │   │   │   └── IngestionViewModel.kt
│   │   │   │   ├── data/
│   │   │   │   │   ├── model/
│   │   │   │   │   │   ├── Workflow.kt
│   │   │   │   │   │   ├── Task.kt
│   │   │   │   │   │   └── Artifact.kt
│   │   │   │   │   ├── repository/
│   │   │   │   │   │   ├── WorkflowRepository.kt
│   │   │   │   │   │   └── FileRepository.kt
│   │   │   │   │   ├── local/
│   │   │   │   │   │   ├── MRWADatabase.kt
│   │   │   │   │   │   └── dao/
│   │   │   │   │   └── remote/
│   │   │   │   │       ├── APIService.kt
│   │   │   │   │       └── WebSocketService.kt
│   │   │   │   ├── worker/
│   │   │   │   │   ├── SyncWorker.kt
│   │   │   │   │   └── WorkflowExecutionWorker.kt
│   │   │   │   └── di/
│   │   │   │       └── AppModule.kt
│   │   │   ├── res/
│   │   │   │   ├── values/
│   │   │   │   ├── drawable/
│   │   │   │   └── xml/
│   │   │   └── AndroidManifest.xml
│   │   ├── test/                    # Unit tests
│   │   └── androidTest/             # Instrumented tests
├── build.gradle.kts                 # Project-level Gradle
└── settings.gradle.kts
```

## Requirements

- **Android Studio**: Hedgehog (2023.1.1) or later
- **Minimum SDK**: API 26 (Android 8.0)
- **Target SDK**: API 34 (Android 14)
- **Kotlin**: 1.9.0 or later
- **Gradle**: 8.2 or later

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/Thimethane/mrwa.git
cd mrwa/platforms/android
```

### 2. Open in Android Studio

```bash
# Open Android Studio and select "Open Project"
# Navigate to platforms/android directory
```

### 3. Sync Gradle Dependencies

```kotlin
// app/build.gradle.kts
dependencies {
    // Jetpack Compose
    implementation("androidx.compose.ui:ui:1.5.4")
    implementation("androidx.compose.material3:material3:1.1.2")
    implementation("androidx.activity:activity-compose:1.8.1")
    
    // ViewModel and LiveData
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.6.2")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.6.2")
    
    // Room Database
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    kapt("androidx.room:room-compiler:2.6.1")
    
    // Retrofit for API calls
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    
    // WebSocket
    implementation("com.squareup.okhttp3:okhttp-ws:4.12.0")
    
    // Dependency Injection (Hilt)
    implementation("com.google.dagger:hilt-android:2.48.1")
    kapt("com.google.dagger:hilt-compiler:2.48.1")
    
    // WorkManager
    implementation("androidx.work:work-runtime-ktx:2.9.0")
    
    // Coil for image loading
    implementation("io.coil-kt:coil-compose:2.5.0")
}
```

### 4. Configure API Endpoint

```kotlin
// app/src/main/java/com/mrwa/data/remote/ApiConfig.kt
object ApiConfig {
    const val BASE_URL = "https://api.mrwa.example.com"
    // For local development:
    // const val BASE_URL = "http://10.0.2.2:8000" // Android emulator
}
```

### 5. Add API Key

```kotlin
// local.properties (not tracked in git)
gemini.api.key=your_api_key_here
```

```kotlin
// app/build.gradle.kts
android {
    defaultConfig {
        val geminiApiKey = project.findProperty("gemini.api.key") ?: ""
        buildConfigField("String", "GEMINI_API_KEY", "\"$geminiApiKey\"")
    }
}
```

### 6. Build and Run

```bash
# Command line
./gradlew assembleDebug
./gradlew installDebug

# Or use Android Studio:
# Run → Run 'app' (Shift+F10)
```

## Architecture

### Clean Architecture with MVVM

```
┌────────────────────────────────────────────┐
│        UI Layer (Jetpack Compose)          │
│  - WorkflowListScreen                      │
│  - WorkflowDetailScreen                    │
│  - ExecutionLogScreen                      │
└───────────────────┬────────────────────────┘
                    │ StateFlow / LiveData
┌───────────────────▼────────────────────────┐
│           ViewModel Layer                   │
│  - WorkflowViewModel                       │
│  - IngestionViewModel                      │
└───────────────────┬────────────────────────┘
                    │ suspend functions
┌───────────────────▼────────────────────────┐
│         Repository Layer                    │
│  - WorkflowRepository (abstraction)        │
│  - FileRepository                          │
└───────────────────┬────────────────────────┘
                    │
      ┌─────────────┴──────────────┐
      │                            │
┌─────▼──────┐           ┌────────▼────────┐
│   Local    │           │     Remote      │
│ Data Source│           │  Data Source    │
│            │           │                 │
│ - Room DB  │           │ - Retrofit API  │
│ - Prefs    │           │ - WebSocket     │
└────────────┘           └─────────────────┘
```

### Key Components

#### 1. WorkflowViewModel

```kotlin
@HiltViewModel
class WorkflowViewModel @Inject constructor(
    private val workflowRepository: WorkflowRepository,
    private val syncService: SyncService
) : ViewModel() {
    
    private val _workflows = MutableStateFlow<List<Workflow>>(emptyList())
    val workflows: StateFlow<List<Workflow>> = _workflows.asStateFlow()
    
    private val _currentWorkflow = MutableStateFlow<Workflow?>(null)
    val currentWorkflow: StateFlow<Workflow?> = _currentWorkflow.asStateFlow()
    
    private val _executionLogs = MutableStateFlow<List<LogEntry>>(emptyList())
    val executionLogs: StateFlow<List<LogEntry>> = _executionLogs.asStateFlow()
    
    fun createWorkflow(config: WorkflowConfig) {
        viewModelScope.launch {
            try {
                val workflow = workflowRepository.createWorkflow(config)
                _workflows.update { it + workflow }
                
                // Subscribe to real-time updates
                subscribeToUpdates(workflow.id)
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
    
    private fun subscribeToUpdates(workflowId: String) {
        viewModelScope.launch {
            syncService.observeWorkflow(workflowId)
                .catch { e -> /* Handle error */ }
                .collect { update ->
                    updateWorkflow(update)
                }
        }
    }
}
```

#### 2. WorkflowRepository

```kotlin
class WorkflowRepository @Inject constructor(
    private val apiService: APIService,
    private val workflowDao: WorkflowDao,
    private val networkMonitor: NetworkMonitor
) {
    suspend fun createWorkflow(config: WorkflowConfig): Workflow {
        return if (networkMonitor.isOnline()) {
            // Create via API
            val workflow = apiService.createWorkflow(config)
            // Cache locally
            workflowDao.insert(workflow.toEntity())
            workflow
        } else {
            // Create locally for offline execution
            val workflow = createOfflineWorkflow(config)
            workflowDao.insert(workflow.toEntity())
            // Queue for sync
            queueForSync(workflow)
            workflow
        }
    }
    
    fun observeWorkflows(): Flow<List<Workflow>> {
        return workflowDao.observeAll()
            .map { entities -> entities.map { it.toModel() } }
    }
}
```

#### 3. WebSocket Service

```kotlin
class WebSocketService @Inject constructor(
    private val okHttpClient: OkHttpClient
) {
    private var webSocket: WebSocket? = null
    private val _updates = MutableSharedFlow<WorkflowUpdate>()
    
    fun connect() {
        val request = Request.Builder()
            .url("wss://api.mrwa.example.com/ws")
            .build()
            
        webSocket = okHttpClient.newWebSocket(request, object : WebSocketListener() {
            override fun onMessage(webSocket: WebSocket, text: String) {
                val update = Json.decodeFromString<WorkflowUpdate>(text)
                _updates.tryEmit(update)
            }
            
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                // Handle reconnection
                scheduleReconnect()
            }
        })
    }
    
    fun observeWorkflow(id: String): Flow<WorkflowUpdate> {
        return _updates.filter { it.workflowId == id }
    }
}
```

## User Interface

### Main Screens with Jetpack Compose

#### 1. Workflow List Screen

```kotlin
@Composable
fun WorkflowListScreen(
    viewModel: WorkflowViewModel = hiltViewModel(),
    onWorkflowClick: (Workflow) -> Unit
) {
    val workflows by viewModel.workflows.collectAsState()
    
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Workflows") })
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { /* Show create dialog */ }) {
                Icon(Icons.Default.Add, "Create workflow")
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.padding(padding)
        ) {
            items(workflows) { workflow ->
                WorkflowCard(
                    workflow = workflow,
                    onClick = { onWorkflowClick(workflow) }
                )
            }
        }
    }
}
```

#### 2. Workflow Detail Screen

```kotlin
@Composable
fun WorkflowDetailScreen(
    workflowId: String,
    viewModel: WorkflowViewModel = hiltViewModel()
) {
    val workflow by viewModel.currentWorkflow.collectAsState()
    val logs by viewModel.executionLogs.collectAsState()
    
    LaunchedEffect(workflowId) {
        viewModel.loadWorkflow(workflowId)
    }
    
    workflow?.let { wf ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            // Status card
            StatusCard(
                stage = wf.stage,
                progress = wf.progress
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Workflow plan
            WorkflowPlanSection(steps = wf.plan)
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Execution logs
            ExecutionLogsSection(logs = logs)
            
            // Artifacts
            if (wf.artifacts.isNotEmpty()) {
                Spacer(modifier = Modifier.height(16.dp))
                ArtifactsSection(artifacts = wf.artifacts)
            }
        }
    }
}
```

#### 3. Status Card Component

```kotlin
@Composable
fun StatusCard(
    stage: WorkflowStage,
    progress: Float
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = stage.color.copy(alpha = 0.1f)
        )
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = stage.icon,
                    contentDescription = null,
                    tint = stage.color
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = stage.name.uppercase(),
                    style = MaterialTheme.typography.titleMedium,
                    color = stage.color
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            LinearProgressIndicator(
                progress = progress,
                modifier = Modifier.fillMaxWidth(),
                color = stage.color
            )
        }
    }
}
```

## Local Storage with Room

### Database Schema

```kotlin
@Database(
    entities = [WorkflowEntity::class, TaskEntity::class, ArtifactEntity::class],
    version = 1,
    exportSchema = false
)
abstract class MRWADatabase : RoomDatabase() {
    abstract fun workflowDao(): WorkflowDao
    abstract fun taskDao(): TaskDao
    abstract fun artifactDao(): ArtifactDao
}

@Entity(tableName = "workflows")
data class WorkflowEntity(
    @PrimaryKey val id: String,
    val name: String,
    val stage: String,
    val progress: Float,
    val createdAt: Long,
    val updatedAt: Long
)

@Dao
interface WorkflowDao {
    @Query("SELECT * FROM workflows ORDER BY createdAt DESC")
    fun observeAll(): Flow<List<WorkflowEntity>>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(workflow: WorkflowEntity)
    
    @Update
    suspend fun update(workflow: WorkflowEntity)
    
    @Delete
    suspend fun delete(workflow: WorkflowEntity)
}
```

## Background Execution

### WorkManager for Reliable Execution

```kotlin
class WorkflowExecutionWorker(
    context: Context,
    params: WorkerParameters,
    private val workflowRepository: WorkflowRepository
) : CoroutineWorker(context, params) {
    
    override suspend fun doWork(): Result {
        val workflowId = inputData.getString("workflow_id") ?: return Result.failure()
        
        return try {
            // Execute workflow in background
            workflowRepository.executeWorkflow(workflowId)
            
            // Show completion notification
            showCompletionNotification(workflowId)
            
            Result.success()
        } catch (e: Exception) {
            if (runAttemptCount < 3) {
                Result.retry()
            } else {
                Result.failure()
            }
        }
    }
    
    private fun showCompletionNotification(workflowId: String) {
        val notification = NotificationCompat.Builder(applicationContext, CHANNEL_ID)
            .setContentTitle("Workflow Complete")
            .setContentText("Your workflow has finished execution")
            .setSmallIcon(R.drawable.ic_notification)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .build()
            
        NotificationManagerCompat.from(applicationContext)
            .notify(workflowId.hashCode(), notification)
    }
}
```

### Scheduling Background Work

```kotlin
fun scheduleWorkflowExecution(workflowId: String) {
    val constraints = Constraints.Builder()
        .setRequiredNetworkType(NetworkType.CONNECTED)
        .build()
        
    val workRequest = OneTimeWorkRequestBuilder<WorkflowExecutionWorker>()
        .setConstraints(constraints)
        .setInputData(workDataOf("workflow_id" to workflowId))
        .build()
        
    WorkManager.getInstance(context).enqueue(workRequest)
}
```

## File Import

### Document Picker Integration

```kotlin
@Composable
fun FileImportButton(
    onFilesSelected: (List<Uri>) -> Unit
) {
    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenMultipleDocuments()
    ) { uris ->
        onFilesSelected(uris)
    }
    
    Button(
        onClick = {
            launcher.launch(arrayOf("application/pdf", "text/plain", "*/*"))
        }
    ) {
        Icon(Icons.Default.Upload, contentDescription = null)
        Spacer(modifier = Modifier.width(8.dp))
        Text("Import Files")
    }
}
```

## Testing

### Unit Tests

```kotlin
@Test
fun `createWorkflow updates workflows state`() = runTest {
    val viewModel = WorkflowViewModel(mockRepository, mockSyncService)
    val config = WorkflowConfig(name = "Test", inputs = emptyList())
    
    viewModel.createWorkflow(config)
    advanceUntilIdle()
    
    val workflows = viewModel.workflows.value
    assertEquals(1, workflows.size)
    assertEquals("Test", workflows.first().name)
}
```

### UI Tests

```kotlin
@Test
fun testWorkflowCreation() {
    composeTestRule.setContent {
        WorkflowListScreen(onWorkflowClick = {})
    }
    
    composeTestRule.onNodeWithText("Create").performClick()
    composeTestRule.onNodeWithText("Workflow Name").performTextInput("Test")
    composeTestRule.onNodeWithText("Create").performClick()
    
    composeTestRule.onNodeWithText("Test").assertExists()
}
```

## Deployment

### Generate Signed APK

```bash
./gradlew assembleRelease
```

### Google Play Console Upload

1. Create release in Play Console
2. Upload APK/AAB
3. Add release notes
4. Submit for review

## Troubleshooting

**Issue**: Build fails with "Unresolved reference"
**Solution**: File → Invalidate Caches → Restart

**Issue**: WebSocket not connecting
**Solution**: Check network security config and cleartext traffic settings

**Issue**: Database migration error
**Solution**: Increment database version and provide migration

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## License

MIT License - see LICENSE file for details.