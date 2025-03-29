package com.daniel.webscrapping.service;

import com.daniel.webscrapping.utils.DownloadUtils;
import com.daniel.webscrapping.utils.FileUtils;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

@Service
public class ScrapingService {

  private static final String BASE_URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos";
  private static final String DOWNLOAD_DIR = "downloads";
  private static final String OUTPUT_DIR = "output";

  public List<String> scrapeAndDownloadAnnexes() {
    List<String> downloadedFiles = new ArrayList<>();

    try {
      // Connect to the webpage
      Document doc = Jsoup.connect(BASE_URL).get();

      // Find PDF links (adjust selector based on actual page structure)
      Elements pdfLinks = doc.select("a[href$=.pdf]");

      // Limit to first two PDFs (Annexes I and II)
      int downloadCount = 0;
      for (Element link : pdfLinks) {
        if (downloadCount >= 2) break;

        String pdfUrl = link.absUrl("href");
        String filename = Paths.get(pdfUrl).getFileName().toString();
        String outputPath = Paths.get(DOWNLOAD_DIR, filename).toString();

        // Download PDF
        if (DownloadUtils.downloadFile(pdfUrl, outputPath)) {
          downloadedFiles.add(outputPath);
          downloadCount++;
        }
      }

      // Compress downloaded files
      String zipPath = Paths.get(OUTPUT_DIR, "annexes.zip").toString();
      FileUtils.compressDirectory(DOWNLOAD_DIR, zipPath);

    } catch (IOException e) {
      e.printStackTrace();
    }

    return downloadedFiles;
  }

}
