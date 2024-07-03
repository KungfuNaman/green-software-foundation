package com.example.ecodocsense.controller;

import com.example.ecodocsense.service.Embeddings;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.embedding.EmbeddingResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
public class EmbeddingsController {
  @Autowired
  Embeddings embedding_service;
  @GetMapping("/ai/getEmbedding")
  public EmbeddingResponse generateStream(@RequestParam(value = "message", defaultValue = "Tell me a joke") String message) {
    return embedding_service.getEmbedding(message);
  }
}
