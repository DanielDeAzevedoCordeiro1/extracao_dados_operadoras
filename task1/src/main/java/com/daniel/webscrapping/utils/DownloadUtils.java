package com.daniel.webscrapping.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URL;
import java.nio.channels.Channels;
import java.nio.channels.ReadableByteChannel;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class DownloadUtils {

  public static Logger logger = LoggerFactory.getLogger(DownloadUtils.class);

  public static boolean downloadFile(String url, String outputPath) {

    try {
      Path directory = Paths.get(outputPath).getParent();


      if (directory != null) Files.createDirectories(directory);

      URL urlObj = new URL(url);
      try (

          ReadableByteChannel rbc = Channels.newChannel(urlObj.openStream());
          FileOutputStream fos = new FileOutputStream(outputPath);

      ) {
        fos.getChannel().transferFrom(rbc, 0, Long.MAX_VALUE);
      }

      logger.info("Download complete.");
      return true;
    } catch (IOException e) {
      e.printStackTrace();
      logger.error(e.getMessage());
      return false;
    }
  }
}
