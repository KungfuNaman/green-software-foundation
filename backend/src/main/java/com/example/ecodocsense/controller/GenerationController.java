package com.example.ecodocsense.controller;

import com.example.ecodocsense.service.Generation;
import java.util.HashMap;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
public class GenerationController {

  @Autowired
  Generation generation_service;
  @GetMapping("/ai/generate")
  public HashMap<String,String> generate(@RequestParam(value = "message", defaultValue = "Tell me a joke") String message) {
    return new HashMap<String,String>() {{
      put("response", generation_service.generateResponse(message));
    }};
  }

  @GetMapping("/ai/generateStream")
  public Flux<ChatResponse> generateStream(@RequestParam(value = "message", defaultValue = "Tell me a joke") String message) {
    return generation_service.generateStream(message);
  }
}
