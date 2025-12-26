# MRWA iOS Application

## Overview

The MRWA iOS app provides a native, high-performance interface for executing and monitoring autonomous AI workflows on iPhone and iPad. Built with SwiftUI and Swift Concurrency, it offers offline-first operation, real-time synchronization, and seamless integration with the MRWA Core engine.

## Features

- ✅ **Native SwiftUI Interface** - Modern, fluid UI following Apple design guidelines
- ✅ **Offline-First Architecture** - Execute workflows without internet connection
- ✅ **Real-Time Sync** - Automatic state synchronization across devices
- ✅ **File Management** - Import from Files, iCloud Drive, and other apps
- ✅ **Push Notifications** - Workflow completion alerts
- ✅ **Widget Support** - View workflow status from home screen
- ✅ **Dark Mode** - Full support for system appearance
- ✅ **Universal App** - Optimized for iPhone, iPad, and Mac (Catalyst)

## Project Structure

```
platforms/ios/
├── README.md                        # This file
├── MRWA.xcodeproj/                  # Xcode project
├── MRWA/                            # Main app target
│   ├── App/
│   │   ├── MRWAApp.swift            # App entry point
│   │   └── AppDelegate.swift        # App lifecycle
│   ├── Views/
│   │   ├── WorkflowListView.swift   # Workflow list
│   │   ├── WorkflowDetailView.swift # Workflow details
│   │   ├── ExecutionLogView.swift   # Real-time logs
│   │   └── SettingsView.swift       # App settings
│   ├── ViewModels/
│   │   ├── WorkflowViewModel.swift  # Workflow state
│   │   └── IngestionViewModel.swift # File ingestion
│   ├── Models/
│   │   ├── Workflow.swift           # Workflow model
│   │   ├── Task.swift               # Task model
│   │   └── Artifact.swift           # Output artifacts
│   ├── Services/
│   │   ├── APIService.swift         # API client
│   │   ├── SyncService.swift        # State synchronization
│   │   └── StorageService.swift     # Local persistence
│   └── Resources/
│       ├── Assets.xcassets/         # Images, colors
│       └── Info.plist               # App configuration
├── MRWAWidget/                      # Widget extension
├── MRWATests/                       # Unit tests
└── MRWAUITests/                     # UI tests
```

## Requirements

- **Xcode**: 15.0 or later
- **iOS**: 16.0 or later (deployment target)
- **Swift**: 5.9 or later
- **Mac**: macOS Sonoma 14.0+ (for development)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/Thimethane/mrwa.git
cd mrwa/platforms/ios
```

### 2. Install Dependencies

```bash
# Using Swift Package Manager (dependencies managed in Xcode)
open MRWA.xcodeproj
# Xcode will automatically resolve dependencies
```

**Swift Package Dependencies**:
- `Alamofire` - HTTP networking
- `SwiftUIX` - Extended SwiftUI components
- `KeychainAccess` - Secure credential storage
- `Kingfisher` - Image downloading and caching

### 3. Configure API Endpoint

```swift
// MRWA/Services/APIService.swift
struct APIConfiguration {
    static let baseURL = "https://api.mrwa.example.com"
    // For local development:
    // static let baseURL = "http://localhost:8000"
}
```

### 4. Add Gemini API Key

```bash
# Create Config.xcconfig file (not tracked in git)
echo "GEMINI_API_KEY = your_api_key_here" > MRWA/Config.xcconfig
```

In Xcode, add `Config.xcconfig` to project settings:
- Select project → Info → Configurations → Debug → MRWA

### 5. Build and Run

```bash
# Command line
xcodebuild -scheme MRWA -destination 'platform=iOS Simulator,name=iPhone 15 Pro' build

# Or use Xcode:
# Cmd+R to build and run
```

## Architecture

### MVVM Pattern with SwiftUI

```
┌─────────────────────────────────────────┐
│              Views (SwiftUI)             │
│  - WorkflowListView                     │
│  - WorkflowDetailView                   │
│  - ExecutionLogView                     │
└──────────────┬──────────────────────────┘
               │ @ObservedObject
               │ @StateObject
┌──────────────▼──────────────────────────┐
│           ViewModels                     │
│  - WorkflowViewModel                    │
│  - IngestionViewModel                   │
└──────────────┬──────────────────────────┘
               │ async/await
               │ Combine publishers
┌──────────────▼──────────────────────────┐
│             Services                     │
│  - APIService (networking)              │
│  - SyncService (state sync)             │
│  - StorageService (Core Data)           │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│            Data Layer                    │
│  - Core Data (local storage)            │
│  - Keychain (credentials)               │
│  - UserDefaults (settings)              │
└─────────────────────────────────────────┘
```

### Key Components

#### 1. WorkflowViewModel

Manages workflow state and execution:

```swift
@MainActor
class WorkflowViewModel: ObservableObject {
    @Published var workflows: [Workflow] = []
    @Published var currentWorkflow: Workflow?
    @Published var executionLogs: [LogEntry] = []
    @Published var isExecuting = false
    
    private let apiService: APIService
    private let syncService: SyncService
    
    func createWorkflow(config: WorkflowConfig) async throws {
        isExecuting = true
        defer { isExecuting = false }
        
        let workflow = try await apiService.createWorkflow(config)
        workflows.append(workflow)
        
        // Subscribe to real-time updates
        await subscribeToUpdates(workflowId: workflow.id)
    }
    
    func subscribeToUpdates(workflowId: String) async {
        for await update in syncService.workflowUpdates(id: workflowId) {
            updateWorkflow(update)
        }
    }
}
```

#### 2. APIService

Handles all network communication:

```swift
actor APIService {
    private let session: URLSession
    private let baseURL: URL
    
    func createWorkflow(_ config: WorkflowConfig) async throws -> Workflow {
        let request = try buildRequest(
            endpoint: "/api/workflows",
            method: "POST",
            body: config
        )
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 201 else {
            throw APIError.invalidResponse
        }
        
        return try JSONDecoder().decode(Workflow.self, from: data)
    }
    
    func uploadFile(_ file: URL) async throws -> FileMetadata {
        let formData = try buildMultipartFormData(file: file)
        // Upload implementation
    }
}
```

#### 3. SyncService

Real-time state synchronization using WebSockets:

```swift
actor SyncService {
    private var webSocket: URLSessionWebSocketTask?
    
    func connect() async throws {
        let url = URL(string: "wss://api.mrwa.example.com/ws")!
        webSocket = URLSession.shared.webSocketTask(with: url)
        webSocket?.resume()
        
        await startListening()
    }
    
    func workflowUpdates(id: String) -> AsyncStream<WorkflowUpdate> {
        AsyncStream { continuation in
            Task {
                for await message in receiveMessages() {
                    if let update = parseWorkflowUpdate(message, id: id) {
                        continuation.yield(update)
                    }
                }
            }
        }
    }
}
```

## User Interface

### Main Screens

#### 1. Workflow List

```swift
struct WorkflowListView: View {
    @StateObject private var viewModel = WorkflowViewModel()
    
    var body: some View {
        NavigationStack {
            List(viewModel.workflows) { workflow in
                NavigationLink(value: workflow) {
                    WorkflowRow(workflow: workflow)
                }
            }
            .navigationTitle("Workflows")
            .navigationDestination(for: Workflow.self) { workflow in
                WorkflowDetailView(workflow: workflow)
            }
            .toolbar {
                Button("New", systemImage: "plus") {
                    showCreateWorkflow = true
                }
            }
        }
    }
}
```

#### 2. Workflow Detail

```swift
struct WorkflowDetailView: View {
    let workflow: Workflow
    @StateObject private var viewModel: WorkflowViewModel
    
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Status card
                StatusCard(stage: workflow.stage)
                
                // Workflow plan
                WorkflowPlanView(steps: workflow.plan)
                
                // Execution log
                ExecutionLogView(logs: viewModel.executionLogs)
                
                // Artifacts
                if !workflow.artifacts.isEmpty {
                    ArtifactsSection(artifacts: workflow.artifacts)
                }
            }
        }
        .navigationTitle(workflow.name)
    }
}
```

#### 3. File Import

```swift
struct FileImportView: View {
    @State private var isImporting = false
    
    var body: some View {
        VStack {
            Button("Import Files") {
                isImporting = true
            }
            .fileImporter(
                isPresented: $isImporting,
                allowedContentTypes: [.pdf, .plainText, .folder],
                allowsMultipleSelection: true
            ) { result in
                handleImport(result)
            }
        }
    }
    
    func handleImport(_ result: Result<[URL], Error>) {
        // Handle file import
    }
}
```

## Local Storage

### Core Data Schema

```swift
@Model
class WorkflowEntity {
    @Attribute(.unique) var id: String
    var name: String
    var stage: String
    var createdAt: Date
    var updatedAt: Date
    
    @Relationship(deleteRule: .cascade)
    var tasks: [TaskEntity]
    
    @Relationship(deleteRule: .cascade)
    var artifacts: [ArtifactEntity]
}

@Model
class TaskEntity {
    var id: String
    var stepNumber: Int
    var description: String
    var status: String
    var startedAt: Date?
    var completedAt: Date?
}
```

## Offline Support

### Offline Execution Strategy

```swift
class OfflineManager {
    func canExecuteOffline(_ config: WorkflowConfig) -> Bool {
        // Check if all required resources are cached
        return config.inputs.allSatisfy { isFileCached($0) }
            && config.requiresAPI == false
    }
    
    func executeOffline(_ config: WorkflowConfig) async throws -> Workflow {
        // Use local MRWA Core engine
        let engine = LocalWorkflowEngine()
        return try await engine.execute(config)
    }
    
    func queueForSync(_ workflow: Workflow) {
        // Queue for upload when connection available
        syncQueue.append(workflow)
    }
}
```

## Push Notifications

### Notification Setup

```swift
// AppDelegate.swift
class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        UNUserNotificationCenter.current()
            .requestAuthorization(options: [.alert, .sound, .badge]) { granted, _ in
                if granted {
                    DispatchQueue.main.async {
                        application.registerForRemoteNotifications()
                    }
                }
            }
        return true
    }
    
    func application(
        _ application: UIApplication,
        didReceiveRemoteNotification userInfo: [AnyHashable: Any]
    ) async -> UIBackgroundFetchResult {
        // Handle workflow completion notification
        if let workflowId = userInfo["workflow_id"] as? String {
            await refreshWorkflow(id: workflowId)
            return .newData
        }
        return .noData
    }
}
```

## Widget Extension

### Workflow Status Widget

```swift
struct WorkflowWidget: Widget {
    let kind = "WorkflowWidget"
    
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            WorkflowWidgetView(entry: entry)
        }
        .configurationDisplayName("Active Workflows")
        .description("View your running workflows")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

struct WorkflowWidgetView: View {
    let entry: Provider.Entry
    
    var body: some View {
        VStack(alignment: .leading) {
            Text(entry.workflow.name)
                .font(.headline)
            
            ProgressView(value: entry.workflow.progress)
            
            Text(entry.workflow.stage.rawValue.uppercased())
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
    }
}
```

## Testing

### Unit Tests

```swift
class WorkflowViewModelTests: XCTestCase {
    var viewModel: WorkflowViewModel!
    var mockAPIService: MockAPIService!
    
    override func setUp() {
        super.setUp()
        mockAPIService = MockAPIService()
        viewModel = WorkflowViewModel(apiService: mockAPIService)
    }
    
    func testCreateWorkflow() async throws {
        let config = WorkflowConfig(name: "Test", inputs: [])
        
        try await viewModel.createWorkflow(config: config)
        
        XCTAssertEqual(viewModel.workflows.count, 1)
        XCTAssertEqual(viewModel.workflows.first?.name, "Test")
    }
}
```

### UI Tests

```swift
class MRWAUITests: XCTestCase {
    func testWorkflowCreation() throws {
        let app = XCUIApplication()
        app.launch()
        
        app.buttons["New"].tap()
        app.textFields["Workflow Name"].tap()
        app.textFields["Workflow Name"].typeText("Test Workflow")
        app.buttons["Create"].tap()
        
        XCTAssertTrue(app.staticTexts["Test Workflow"].exists)
    }
}
```

## Performance Optimization

- **Image Caching**: Use Kingfisher for efficient image loading
- **Lazy Loading**: Load workflow details on demand
- **Background Tasks**: Use Background Tasks framework for sync
- **Memory Management**: Proper use of `weak` and `unowned` references

## Deployment

### TestFlight Distribution

```bash
# Archive for distribution
xcodebuild -scheme MRWA \
  -archivePath ./build/MRWA.xcarchive \
  -configuration Release \
  archive

# Export IPA
xcodebuild -exportArchive \
  -archivePath ./build/MRWA.xcarchive \
  -exportPath ./build \
  -exportOptionsPlist ExportOptions.plist
```

### App Store Submission

1. Update version in `Info.plist`
2. Create screenshots using `fastlane snapshot`
3. Upload via Xcode or Transporter
4. Submit for review

## Troubleshooting

### Common Issues

**Issue**: Build fails with "Package resolution error"
**Solution**: File → Packages → Reset Package Caches

**Issue**: Real-time sync not working
**Solution**: Check WebSocket connection and firewall settings

**Issue**: Files not importing
**Solution**: Verify app has permission in Settings → Privacy → Files

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## License

MIT License - see LICENSE file for details.