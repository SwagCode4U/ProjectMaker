# backend/app/services/frameworks/backend/springboot.py
from pathlib import Path
from typing import Dict


def normalize(v: str) -> str:
    return 'springboot'


def meta() -> Dict:
    return {'id': 'springboot', 'port': 8080}


def preview(config: Dict) -> Dict:
    name = config.get('backend_folder_name', 'backend')
    # Show Gradle Spring Boot structure under the backend folder
    return {
        'name': name,
        'type': 'directory',
        'children': [
            {'name': 'build.gradle', 'type': 'file'},
            {'name': 'settings.gradle', 'type': 'file'},
            {'name': 'README.md', 'type': 'file'},
            {
                'name': 'src', 'type': 'directory', 'children': [
                    {
                        'name': 'main', 'type': 'directory', 'children': [
                            {
                                'name': 'java', 'type': 'directory', 'children': [
                                    {'name': 'com/example', 'type': 'directory', 'children': [
                                        {'name': 'SpringBootBoilerplateApplication.java', 'type': 'file'},
                                        {'name': 'config', 'type': 'directory', 'children': [
                                            {'name': 'WebSocketConfig.java', 'type': 'file'}
                                        ]},
                                        {'name': 'controller', 'type': 'directory', 'children': [
                                            {'name': 'MessageController.java', 'type': 'file'}
                                        ]},
                                        {'name': 'model', 'type': 'directory', 'children': [
                                            {'name': 'Message.java', 'type': 'file'}
                                        ]},
                                    ]}
                                ]
                            },
                            {
                                'name': 'resources', 'type': 'directory', 'children': [
                                    {'name': 'application.properties', 'type': 'file'},
                                    {'name': 'static', 'type': 'directory', 'children': [
                                        {'name': 'index.html', 'type': 'file'}
                                    ]}
                                ]
                            }
                        ]
                    },
                    {'name': 'test', 'type': 'directory', 'children': [
                        {'name': 'java/com/example', 'type': 'directory'}
                    ]}
                ]
            }
        ]
    }


def build(root: Path, config: Dict) -> Dict:
    backend = config.get('backend_folder_name', 'backend')
    base = root / backend
    ops, errs = [], []
    try:
        # Create directory tree
        (base / 'src' / 'main' / 'java' / 'com' / 'example' / 'config').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'main' / 'java' / 'com' / 'example' / 'controller').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'main' / 'java' / 'com' / 'example' / 'model').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'main' / 'resources' / 'static').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'test' / 'java' / 'com' / 'example').mkdir(parents=True, exist_ok=True)

        files: Dict[str, str] = {
            'build.gradle': """plugins {
    id 'org.springframework.boot' version '3.1.0'
    id 'io.spring.dependency-management' version '1.0.12.RELEASE'
    id 'java'
}

group = 'com.example'
version = '0.0.1-SNAPSHOT'
sourceCompatibility = '17'

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-websocket'
    implementation 'org.springframework.boot:spring-boot-starter'
    implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}

tasks.named('test') {
    useJUnitPlatform()
}
""",
            'settings.gradle': """rootProject.name = 'spring-boot-boilerplate'\n""",
            'src/main/java/com/example/SpringBootBoilerplateApplication.java': """package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SpringBootBoilerplateApplication {
    public static void main(String[] args) {
        SpringApplication.run(SpringBootBoilerplateApplication.class, args);
    }
}
""",
            'src/main/java/com/example/config/WebSocketConfig.java': """package com.example.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;
import com.example.controller.MessageController;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {
    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(new MessageController(), "/ws").setAllowedOrigins("*");
    }
}
""",
            'src/main/java/com/example/controller/MessageController.java': """package com.example.controller;

import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

public class MessageController extends TextWebSocketHandler {
    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) {
        try {
            session.sendMessage(new TextMessage("Echo: " + message.getPayload()));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
""",
            'src/main/java/com/example/model/Message.java': """package com.example.model;

public class Message {
    private String content;

    public Message(String content) {
        this.content = content;
    }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
}
""",
            'src/main/resources/application.properties': """server.port=8080\n""",
'README.md': """# Spring Boot Boilerplate

A starter Spring Boot project with WebSocket echo handler.

## Getting Started
```bash
./gradlew bootRun  # or: ./mvnw spring-boot:run
```

---

Generated with [ProjectMaker](https://github.com/SwagCode4U/projectmaker)
""",
            'src/main/resources/static/index.html': """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Spring Boot WebSocket</title>
</head>
<body>
  <div id=\"app\">Spring Boot WebSocket is running.</div>
</body>
</html>
""",
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {backend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return {'operations': ops, 'errors': errs, 'backend_type': 'springboot'}
