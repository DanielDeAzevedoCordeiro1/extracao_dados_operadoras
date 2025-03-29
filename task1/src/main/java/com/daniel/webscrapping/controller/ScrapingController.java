package com.daniel.webscrapping.controller;

import com.daniel.webscrapping.service.ScrapingService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("api/scraping")
public class ScrapingController {

  private final ScrapingService scrapingService;

  public ScrapingController(ScrapingService scrapingService) {
    this.scrapingService = scrapingService;
  }

  @GetMapping("/download-attachments")
  public List<String> downloadAnnexes() {
    return scrapingService.scrapeAndDownloadAnnexes();
  }
}
