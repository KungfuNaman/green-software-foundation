package com.example.ecodocsense.service;

import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.ollama.OllamaChatModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

@Service
public class Generation {

  private final OllamaChatModel chatModel;

  @Autowired
  public Generation(OllamaChatModel chatModel) {
    this.chatModel = chatModel;
  }

  public String generateResponse(String input) {
        return chatModel.call(input);
    }
    public Flux<ChatResponse> generateStream(String input) {
      Prompt prompt = new Prompt(new UserMessage(input));
      return chatModel.stream(prompt);
    }
}
