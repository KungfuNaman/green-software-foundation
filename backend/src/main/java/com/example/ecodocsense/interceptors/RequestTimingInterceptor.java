package com.example.ecodocsense.interceptors;


import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

@Component
public class RequestTimingInterceptor implements HandlerInterceptor {

  private static final String START_TIME_ATTRIBUTE = "startTime";

  public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
    request.setAttribute(START_TIME_ATTRIBUTE, System.currentTimeMillis());
    return true;
  }

  public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
    long startTime = (Long) request.getAttribute(START_TIME_ATTRIBUTE);
    long endTime = System.currentTimeMillis();
    long duration = endTime - startTime;
    response.addHeader("X-Processing-Time", duration + "ms");
  }
}

