package com.example.ecodocsense.service;

import java.util.Arrays;
import java.util.List;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.embedding.EmbeddingRequest;
import org.springframework.ai.embedding.EmbeddingResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class Embeddings {
  private final EmbeddingModel embeddingModel;

  @Autowired
  public Embeddings(EmbeddingModel embeddingModel) {
    this.embeddingModel = embeddingModel;
  }
  public EmbeddingResponse getEmbedding(String input) {
    return this.embeddingModel.embedForResponse(Arrays.asList(input));
  }

}
