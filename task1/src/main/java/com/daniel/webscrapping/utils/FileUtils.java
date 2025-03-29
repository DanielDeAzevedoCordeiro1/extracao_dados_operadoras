package com.daniel.webscrapping.utils;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

public class FileUtils {

  public static boolean compressDirectory(String sourceDir, String outputZipPath) {
    try {
      // Ensure output directory exists
      Path outputPath = Paths.get(outputZipPath);
      Files.createDirectories(outputPath.getParent());

      // Create ZIP output stream
      try (
          FileOutputStream fos = new FileOutputStream(outputZipPath);
          ZipOutputStream zos = new ZipOutputStream(fos)
      ) {
        File sourceDirFile = new File(sourceDir);
        compressDirectoryToZipMethod(sourceDirFile, sourceDirFile.getName(), zos);
      }
      return true;
    } catch (IOException e) {
      e.printStackTrace();
      return false;
    }
  }


  private static void compressDirectoryToZipMethod(File sourceFile, String parentDir, ZipOutputStream zos) throws IOException {
    if (sourceFile.isDirectory()) {
      File[] files = sourceFile.listFiles();
      if (files != null) {
        for (File file : files) {
          String path = parentDir + "/" + file.getName();
          if (file.isDirectory()) {
            compressDirectoryToZipMethod(file, path, zos);
          } else {
            addToZip(file, path, zos);
          }
        }
      }
    } else {
      addToZip(sourceFile, sourceFile.getName(), zos);
    }
  }

  private static void addToZip(File file, String fileName, ZipOutputStream zos) throws IOException {
    try (FileInputStream fis = new FileInputStream(file)) {
      ZipEntry zipEntry = new ZipEntry(fileName);
      zos.putNextEntry(zipEntry);

      byte[] bytes = new byte[1024];
      int length;
      while ((length = fis.read(bytes)) >= 0) {
        zos.write(bytes, 0, length);
      }
      zos.closeEntry();
    }
  }
}
