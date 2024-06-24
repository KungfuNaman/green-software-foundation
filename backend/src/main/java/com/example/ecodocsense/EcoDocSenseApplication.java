package com.example.ecodocsense;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * The entry point for the EcoDocSense Spring Boot application.
 */

@SpringBootApplication
public class EcoDocSenseApplication {

  /**
   * The main method which serves as the entry point for the Spring Boot application.
   *
   * @param args command line arguments
   */
  @SuppressWarnings("checkstyle:FileTabCharacter")
  public static void main(String[] args) {
    SpringApplication.run(EcoDocSenseApplication.class, args);
  }
}
