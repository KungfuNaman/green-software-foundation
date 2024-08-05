
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import 'jspdf-autotable';
import logo from '../assets/GSFLogo.jpg'; // Ensure this path is correct

// Function to draw the header and footer
const drawHeaderFooter = (doc, pageNumber, totalPages) => {
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  
  // Header
  doc.setFillColor(0, 51, 51); // Dark green color
  doc.rect(0, 0, pageWidth, 15, 'F');
  
  // Footer
  const footerY = pageHeight - 15;
  const date = new Date().toLocaleDateString('en-GB'); // Format date as dd/mm/yyyy
  const footerText = 'Green Software Foundation, Inc. or its affiliates. All rights reserved.';
  
  doc.setFillColor(0, 51, 51); // Dark green color
  doc.rect(0, footerY, pageWidth, 15, 'F');
  doc.setTextColor(255, 255, 255); // White color for text
  doc.setFontSize(10);
  doc.setFont('Arial', 'normal'); // Ensure text is not bold
  doc.text(date, 10, footerY + 10);
  doc.addImage(logo, 'JPEG', 45, footerY + 2, 15, 11); // Adjust logo size and position
  doc.text(footerText, 65, footerY + 10);
  doc.text(`Page ${pageNumber} of ${totalPages}`, pageWidth - 40, footerY + 10); // Adjust page number position
};

// Function to draw a light green leaf background
const drawLeafBackground = (doc) => {
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  doc.setFillColor(230, 255, 230); // Light green color
  doc.rect(0, 0, pageWidth, pageHeight, 'F');
};

// Function to draw a box around the content
const drawBox = (doc, yOffset) => {
  const pageWidth = doc.internal.pageSize.getWidth();
  const margin = 10;
  const boxHeight = yOffset - margin;
  doc.setLineWidth(0.5);
  doc.rect(margin, margin + 20, pageWidth - 2 * margin, boxHeight);
};

// Function to draw a single query
const drawQuery = (doc, data, yOffset) => {
  const pageWidth = doc.internal.pageSize.getWidth();
  const lineHeight = 10;
  const margin = 20;
  const maxWidth = pageWidth - margin * 2;

  // Define content
  const content = [
    { title: 'Query:', text: data.query },
    { title: 'Practice:', text: data.practice },
    { title: 'Explanation:', text: data.explanation },
    { title: 'Result:', text: data.result },
    { title: 'Suggestion:', text: data.result === 'No' ? `Please ${data.practice}` : '-' }
  ];
  
  // Draw each content
  content.forEach((item, index) => {
    doc.setFont('Arial', 'bold');
    doc.setFontSize(14);
    doc.setTextColor(0, 0, 0); // Black text color
    doc.text(item.title, margin, yOffset);
    
    doc.setFont('Arial', 'normal');
    doc.setFontSize(14);
    const textLines = doc.splitTextToSize(item.text, maxWidth - 30); // Adjust width for text wrapping
    doc.text(textLines, margin + 30, yOffset);
    yOffset += lineHeight * textLines.length + 5; // Adjust space between sections
    
    // Reduce space between Explanation and Result
    if (index === 2) {
      yOffset += 5;
    }
  });

  return yOffset;
};

const generatePDF = async (analysisData, charts) => {
  const { progressValue, categoryWiseResult, apiResponse, docName } = analysisData;
  const doc = new jsPDF();
  let pageNumber = 1;

  // Calculate total pages for footer
  const totalPages = apiResponse.length + 3; // 1 for title page, 1 for graphical evaluation, 1 for ranking, and 1 for each query

  // Draw background, box, and header/footer on the first page
  drawLeafBackground(doc);
  drawHeaderFooter(doc, pageNumber, totalPages);

  // Add the main title on the first page
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  doc.setFillColor(0, 51, 51); // Dark green color for rectangle
  doc.rect(10, pageHeight / 2 - 20, pageWidth - 20, 30, 'F');
  doc.setTextColor(230, 255, 230); // Light green color for text
  doc.setFont('Arial', 'bold');
  doc.setFontSize(22);
  doc.text('Eco Doc Sustainability Report', pageWidth / 2, pageHeight / 2, { align: 'center' });

  // Ensure subsequent text is black
  doc.setTextColor(0, 0, 0);

  // Add a new page for Graphical Evaluation
  doc.addPage();
  pageNumber++;
  drawLeafBackground(doc);
  drawHeaderFooter(doc, pageNumber, totalPages);

  // Add Graphical Evaluation
  doc.setFont('Arial', 'bold');
  doc.setFontSize(14);
  doc.setTextColor(0, 0, 0); // Black text color
  doc.text('Graphical Evaluation', 10, 20);
  doc.setFont('Arial', 'normal');

  let yOffset = 30;
  for (let i = 0; i < charts.length; i++) {
    const chartCanvas = await html2canvas(charts[i]);
    const imgData = chartCanvas.toDataURL('image/png');
    doc.addImage(imgData, 'PNG', 10, yOffset, 180, 60); // Adjust the size of the charts
    yOffset += 70;
    if (i < charts.length - 1 && yOffset > 240) {
      doc.addPage();
      pageNumber++;
      drawLeafBackground(doc);
      drawHeaderFooter(doc, pageNumber, totalPages);
      yOffset = 20;
    }
  }

  // Add Evaluation section
  doc.addPage();
  pageNumber++;
  drawLeafBackground(doc);
  drawHeaderFooter(doc, pageNumber, totalPages);
  doc.setFont('Arial', 'bold');
  doc.setFontSize(14);
  doc.setTextColor(0, 0, 0); // Black text color
  doc.text('Evaluation', 10, 30); // Evaluation heading outside the table
  doc.setFont('Arial', 'normal');

  apiResponse.forEach((item, index) => {
    if (index > 0) {
      doc.addPage();
      pageNumber++;
      drawLeafBackground(doc);
      drawHeaderFooter(doc, pageNumber, totalPages);
    }
    yOffset = 40;
    yOffset = drawQuery(doc, item, yOffset);
    drawBox(doc, yOffset);
  });

  // Add Ranking of document based on Sustainability
  doc.addPage();
  pageNumber++;
  drawLeafBackground(doc);
  drawHeaderFooter(doc, pageNumber, totalPages);
  doc.setFont('Arial', 'bold');
  doc.setFontSize(14);
  doc.setTextColor(0, 0, 0); // Black text color
  doc.text('Ranking of document based on Sustainability', 10, 20);
  doc.setFont('Arial', 'normal');

  yOffset = 30;
  const rank = `${apiResponse.filter(practice => practice.result === 'Yes').length}/${apiResponse.length}`;
  doc.text(`Rank: ${rank}`, 10, yOffset);

  // Save the PDF
  doc.save(`${docName}_Sustainability_Report.pdf`);
};

export default generatePDF;

