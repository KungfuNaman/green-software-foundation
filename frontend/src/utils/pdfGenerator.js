
// import jsPDF from 'jspdf';
// import 'jspdf-autotable';
// import logo from '../assets/GSFLogo.jpg'; // Ensure this path is correct
// import UberFront from '../assets/UberFront.jpg'; // Ensure this path is correct

// // Function to draw the footer
// const drawFooter = (doc, pageNumber, totalPages) => {
//   const pageWidth = doc.internal.pageSize.getWidth();
//   const pageHeight = doc.internal.pageSize.getHeight();

//   // Footer
//   const footerY = pageHeight - 15;
//   const date = new Date().toLocaleDateString('en-GB'); // Format date as dd/mm/yyyy
//   const footerText = 'Green Software Foundation, Inc. or its affiliates. All rights reserved.';

//   doc.setFillColor(0, 51, 51); // Dark green color
//   doc.rect(0, footerY, pageWidth, 15, 'F');
//   doc.setTextColor(255, 255, 255); // White color for text
//   doc.setFontSize(10);
//   doc.setFont('Arial', 'normal'); // Ensure text is not bold
//   doc.text(date, 10, footerY + 10);
//   doc.addImage(logo, 'JPEG', 45, footerY + 2, 15, 11); // Adjust logo size and position
//   doc.text(footerText, 65, footerY + 10);
//   doc.text(`Page ${pageNumber} of ${totalPages}`, pageWidth - 30, footerY + 10); // Adjust page number position
// };

// // Function to draw a box around the content
// const drawBox = (doc, yOffset) => {
//   const pageWidth = doc.internal.pageSize.getWidth();
//   const margin = 10;
//   const boxHeight = yOffset - margin;
//   doc.setLineWidth(0.5);
//   doc.rect(margin, margin + 20, pageWidth - 2 * margin, boxHeight);
// };

// // Function to draw a single query
// const drawQuery = (doc, data, yOffset) => {
//   const pageWidth = doc.internal.pageSize.getWidth();
//   const lineHeight = 10;
//   const margin = 20;
//   const maxWidth = pageWidth - margin * 2;

//   // Define content
//   const content = [
//     { title: 'Query:', text: data.query },
//     { title: 'Practice:', text: data.practice },
   
//     { title: 'Result:', text: data.result },
//     { title: 'Suggestion:', text: data.result === 'No' ? `Please ${data.practice}` : '-' },
//     { title: 'Explanation:', text: data.explanation }
//   ];

//   // Draw each content
//   content.forEach((item, index) => {
//     doc.setFont('Arial', 'bold');
//     doc.setFontSize(14);
//     doc.setTextColor(0, 0, 0); // Black text color
//     doc.text(item.title, margin, yOffset);

//     doc.setFont('Arial', 'normal');
//     doc.setFontSize(14);
//     const textLines = doc.splitTextToSize(item.text, maxWidth - 30); // Adjust width for text wrapping
//     doc.text(textLines, margin + 30, yOffset);
//     yOffset += lineHeight * textLines.length + 9; // Adjust space between sections
//   });

//   return yOffset;
// };

// // Function to add summary page
// const addSummaryPage = (doc) => {
//   const summaryText = `The project, EcoDoc Sense, is focused on incorporating sustainability into the software design phase to address the significant environmental impact of software development and usage. Traditionally, the environmental impact of software is assessed after development and deployment, using metrics such as CPU utilization and memory usage. This project aims to shift this assessment to the design phase, allowing developers to consider sustainability alongside other factors like cost and performance.
  
//   To achieve this, the project employs a methodology that involves ranking software architecture documents based on their adherence to green practices. These practices are categorized into different areas, including resource optimization, data efficiency, performance management, security, and user impact. Specific examples of green practices include minimizing the number of deployed environments, optimizing storage utilization, and optimizing average CPU utilization.
  
//   The ranking of documents is based on the identified green practices. This project ultimately aims to guide software developers in integrating sustainable practices into their designs, contributing to greener software solutions.`;

//   doc.addPage();
//   doc.setFont('Arial', 'bold');
//   doc.setFontSize(16);
//   doc.setTextColor(0, 0, 0); // Black text color
//   doc.text('About the Sustainability Report', doc.internal.pageSize.getWidth() / 2, 20, { align: 'center' });

//   doc.setFont('Arial', 'normal');
//   doc.setFontSize(12);
//   doc.setTextColor(0, 0, 0); // Black text color
//   const lines = doc.splitTextToSize(summaryText, doc.internal.pageSize.getWidth() - 40);
//   doc.text(lines, 20, 40);
// };

// // Function to add table of contents page
// const addTableOfContentsPage = (doc, pageNumbers) => {
//   doc.addPage();
//   doc.setFont('Arial', 'bold');
//   doc.setFontSize(16);
//   doc.setTextColor(0, 0, 0); // Black text color
//   doc.text('Table of contents', doc.internal.pageSize.getWidth() / 2, 20, { align: 'center' });

//   doc.setFont('Arial', 'normal');
//   doc.setFontSize(12);
//   doc.setTextColor(0, 0, 0); // Black text color
//   const tocContent = [
//     { title: 'About the Sustainability Report', page: pageNumbers.summary },
//     { title: 'Graphical Evaluation', page: pageNumbers.graphicalEvaluation },
//     { title: 'Ranking of Document', page: pageNumbers.ranking },
//     { title: 'Evaluation', page: pageNumbers.evaluation }
//   ];

//   tocContent.forEach((item, index) => {
//     doc.text(item.title, 20, 40 + (index * 10));
//     doc.text(`${item.page}`, doc.internal.pageSize.getWidth() - 20, 40 + (index * 10), { align: 'right' });
//   });
// };

// const generatePDF = async (analysisData) => {
//   const { progressValue, categoryWiseResult, apiResponse, docName } = analysisData;
//   const doc = new jsPDF();
//   let pageNumber = 1;

//   // Calculate total pages for footer
//   const totalPages = apiResponse.length + 3; // 1 for title page, 1 for summary, 1 for table of contents, 1 for graphical evaluation, 1 for ranking, and 1 for each query

//   // Draw the title page with a dark green box and white text
//   const pageWidth = doc.internal.pageSize.getWidth();
//   const pageHeight = doc.internal.pageSize.getHeight();
//   doc.setFillColor(0, 51, 51); // Dark green color for rectangle
//   doc.rect(10, pageHeight / 2 - 20, pageWidth - 20, 30, 'F');
//   doc.setTextColor(230, 255, 230); // Light green color for text
//   doc.setFont('Arial', 'bold');
//   doc.setFontSize(22);
//   doc.text('Eco Doc Sustainability Report', pageWidth / 2, pageHeight / 2, { align: 'center' });

//   // Ensure subsequent text is black
//   doc.setTextColor(0, 0, 0);
//   drawFooter(doc, pageNumber, totalPages);

//   // Add summary page
//   addSummaryPage(doc);
//   const summaryPageNumber = pageNumber + 1;
//   pageNumber++;
//   drawFooter(doc, pageNumber, totalPages);

//   // Add table of contents page
//   addTableOfContentsPage(doc, {
//     summary: summaryPageNumber,
//     graphicalEvaluation: summaryPageNumber + 2,
//     ranking: summaryPageNumber + 3,
//     evaluation: summaryPageNumber + 4
//   });
//   pageNumber++;
//   drawFooter(doc, pageNumber, totalPages);

//   // Add a new page for Graphical Evaluation
//   doc.addPage();
//   pageNumber++;
//   drawFooter(doc, pageNumber, totalPages);

//   // Add Graphical Evaluation
//   doc.setFont('Arial', 'bold');
//   doc.setFontSize(14);
//   doc.setTextColor(0, 0, 0); // Black text color
//   doc.text('Graphical Evaluation', 10, 20);
//   doc.setFont('Arial', 'normal');

//   let yOffset = 30;
//   const imgData = UberFront;
//   doc.addImage(imgData, 'JPEG', 10, yOffset, 180, 160); // Adjust the size of the image
//   yOffset += 170;

//   // Add Ranking of document based on Sustainability
//   doc.addPage();
//   pageNumber++;
//   drawFooter(doc, pageNumber, totalPages);
//   doc.setFont('Arial', 'bold');
//   doc.setFontSize(14);
//   doc.setTextColor(0, 0, 0); // Black text color
//   doc.text('Ranking of document based on Sustainability', 10, 20);
//   doc.setFont('Arial', 'normal');

//   yOffset = 30;
//   const rank = `${apiResponse.filter(practice => practice.result === 'Yes').length}/${apiResponse.length}`;
//   doc.text(`Rank: ${rank}`, 10, yOffset);

//   // Generate the table content
//   const tableData = {
//     'Resource Optimization': { followed: [], notFollowed: [] },
//     'Data Efficiency': { followed: [], notFollowed: [] },
//     'Performance Management': { followed: [], notFollowed: [] },
//     'Security': { followed: [], notFollowed: [] },
//     'User Impact': { followed: [], notFollowed: [] }
//   };

//   apiResponse.forEach((practice) => {
//     const category = practice.category;
//     if (practice.result === 'Yes') {
//       tableData[category].followed.push(practice.practice);
//     } else {
//       tableData[category].notFollowed.push(practice.practice);
//     }
//   });

//   // Define table headers
//   const headers = [
//     { title: 'Categories', dataKey: 'category' },
//     { title: 'Practices being followed', dataKey: 'followed' },
//     { title: 'Practices not followed', dataKey: 'notFollowed' }
//   ];

//   // Prepare table rows
//   const rows = [];
//   Object.keys(tableData).forEach((category) => {
//     rows.push({
//       category,
//       followed: tableData[category].followed.join(', '),
//       notFollowed: tableData[category].notFollowed.join(', ')
//     });
//   });

//   // Draw the table
//   yOffset += 20;
//   doc.setFontSize(10);
//   doc.autoTable({
//     startY: yOffset,
//     head: [headers],
//     body: rows.map(row => [row.category, row.followed, row.notFollowed]),
//     margin: { left: 10, right: 10 },
//     styles: {
//       fontSize: 10,
//       textColor: [0, 0, 0], // black text color
//       lineColor: [0, 0, 0], // black border color
//       lineWidth: 0.1,
//     },
//     headStyles: {
//       fillColor: [200, 200, 200], // light gray background for header
//     },
//   });

//   // Add Evaluation section
//   doc.addPage();
//   pageNumber++;
//   drawFooter(doc, pageNumber, totalPages);
//   doc.setFont('Arial', 'bold');
//   doc.setFontSize(14);
//   doc.setTextColor(0, 0, 0); // Black text color
//   doc.text('Evaluation', 10, 25); // Evaluation heading outside the table
//   doc.setFont('Arial', 'normal');

//   apiResponse.forEach((item, index) => {
//     if (index > 0) {
//       doc.addPage();
//       pageNumber++;
//       drawFooter(doc, pageNumber, totalPages);
//     }
//     yOffset = 40;
//     yOffset = drawQuery(doc, item, yOffset);
//    // yOffset -= 5; // Reduced space between Explanation and Result
//     drawBox(doc, yOffset);
//   });

//   // Save the PDF
//   doc.save(`${docName}_Sustainability_Report.pdf`);
// };

// export const handleDownloadPDF = (analysisData) => {
//   generatePDF(analysisData);
// };

// export default generatePDF;

import jsPDF from 'jspdf';
import 'jspdf-autotable';
import logo from '../assets/GSFLogo.jpg'; // Ensure this path is correct
import UberFront from '../assets/UberFront.jpg'; // Ensure this path is correct

// Function to draw the footer
const drawFooter = (doc, pageNumber, totalPages) => {
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();

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
  doc.text(`Page ${pageNumber} of ${totalPages}`, pageWidth - 30, footerY + 10); // Adjust page number position
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
    { title: 'Result:', text: data.result },
    { title: 'Suggestion:', text: data.result === 'No' ? `Please ${data.practice}` : '-' },
    { title: 'Explanation:', text: data.explanation }
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
    yOffset += lineHeight * textLines.length + 9; // Adjust space between sections
  });

  return yOffset;
};

// Function to add summary page
const addSummaryPage = (doc) => {
  const summaryText = `The project, EcoDoc Sense, is focused on incorporating sustainability into the software design phase to address the significant environmental impact of software development and usage. Traditionally, the environmental impact of software is assessed after development and deployment, using metrics such as CPU utilization and memory usage. This project aims to shift this assessment to the design phase, allowing developers to consider sustainability alongside other factors like cost and performance.
  
  To achieve this, the project employs a methodology that involves ranking software architecture documents based on their adherence to green practices. These practices are categorized into different areas, including resource optimization, data efficiency, performance management, security, and user impact. Specific examples of green practices include minimizing the number of deployed environments, optimizing storage utilization, and optimizing average CPU utilization.
  
  The ranking of documents is based on the identified green practices. This project ultimately aims to guide software developers in integrating sustainable practices into their designs, contributing to greener software solutions.`;

  doc.addPage();
  doc.setFont('Arial', 'bold');
  doc.setFontSize(16);
  doc.setTextColor(0, 0, 0); // Black text color
  doc.text('About the Sustainability Report', doc.internal.pageSize.getWidth() / 2, 20, { align: 'center' });

  doc.setFont('Arial', 'normal');
  doc.setFontSize(12);
  doc.setTextColor(0, 0, 0); // Black text color
  const lines = doc.splitTextToSize(summaryText, doc.internal.pageSize.getWidth() - 40);
  doc.text(lines, 20, 40);
};

// Function to add table of contents page
const addTableOfContentsPage = (doc, pageNumbers) => {
  doc.addPage();
  doc.setFont('Arial', 'bold');
  doc.setFontSize(16);
  doc.setTextColor(0, 0, 0); // Black text color
  doc.text('Table of contents', doc.internal.pageSize.getWidth() / 2, 20, { align: 'center' });

  doc.setFont('Arial', 'normal');
  doc.setFontSize(12);
  doc.setTextColor(0, 0, 0); // Black text color
  const tocContent = [
    { title: 'About the Sustainability Report', page: pageNumbers.summary },
    { title: 'Graphical Evaluation', page: pageNumbers.graphicalEvaluation },
    { title: 'Ranking of Document', page: pageNumbers.ranking },
    { title: 'Evaluation', page: pageNumbers.evaluation }
  ];

  tocContent.forEach((item, index) => {
    doc.text(item.title, 20, 40 + (index * 10));
    doc.text(`${item.page}`, doc.internal.pageSize.getWidth() - 20, 40 + (index * 10), { align: 'right' });
  });
};

const generatePDF = async (analysisData) => {
  const { progressValue, categoryWiseResult, apiResponse, docName } = analysisData;
  const doc = new jsPDF();
  let pageNumber = 1;

  // Calculate total pages for footer
  const totalPages = apiResponse.length + 3; // 1 for title page, 1 for summary, 1 for table of contents, 1 for graphical evaluation, 1 for ranking, and 1 for each query

  // Draw the title page with a dark green box and white text
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
  drawFooter(doc, pageNumber, totalPages);

  // Add summary page
  addSummaryPage(doc);
  const summaryPageNumber = pageNumber + 1;
  pageNumber++;
  drawFooter(doc, pageNumber, totalPages);

  // Add table of contents page
  addTableOfContentsPage(doc, {
    summary: summaryPageNumber,
    graphicalEvaluation: summaryPageNumber + 2,
    ranking: summaryPageNumber + 3,
    evaluation: summaryPageNumber + 4
  });
  pageNumber++;
  drawFooter(doc, pageNumber, totalPages);

  // Add a new page for Graphical Evaluation
  doc.addPage();
  pageNumber++;
  drawFooter(doc, pageNumber, totalPages);

  // Add Graphical Evaluation
  doc.setFont('Arial', 'bold');
  doc.setFontSize(14);
  doc.setTextColor(0, 0, 0); // Black text color
  doc.text('Graphical Evaluation', 10, 20);
  doc.setFont('Arial', 'normal');

  let yOffset = 30;
  const imgData = UberFront;
  doc.addImage(imgData, 'JPEG', 10, yOffset, 180, 160); // Adjust the size of the image
  yOffset += 170;

  // Add Ranking of document based on Sustainability
  doc.addPage();
  pageNumber++;
  drawFooter(doc, pageNumber, totalPages);
  doc.setFont('Arial', 'bold');
  doc.setFontSize(14);
  doc.setTextColor(0, 0, 0); // Black text color
  doc.text('Ranking of document based on Sustainability', 10, 20);
  doc.setFont('Arial', 'normal');

  yOffset = 30;
  const rank = `${apiResponse.filter(practice => practice.result === 'Yes').length}/${apiResponse.length}`;
  doc.text(`Rank: ${rank}`, 10, yOffset);

  // Generate the table content
  const tableData = {
    'Resource Optimization': { followed: [], notFollowed: [] },
    'Data Efficiency': { followed: [], notFollowed: [] },
    'Performance Management': { followed: [], notFollowed: [] },
    'Security': { followed: [], notFollowed: [] },
    'User Impact': { followed: [], notFollowed: [] }
  };

  apiResponse.forEach((practice) => {
    const category = practice.category;
    if (practice.result === 'Yes') {
      tableData[category].followed.push(practice.practice);
    } else {
      tableData[category].notFollowed.push(practice.practice);
    }
  });

  // Define table headers
  const headers = [
    { title: 'Categories', dataKey: 'category' },
    { title: 'Practices being followed', dataKey: 'followed' },
    { title: 'Count of Practices being followed', dataKey: 'followedCount' },
    { title: 'Practices not followed', dataKey: 'notFollowed' },
    { title: 'Count of Practices not followed', dataKey: 'notFollowedCount' }
  ];

  // Prepare table rows
  const rows = [];
  Object.keys(tableData).forEach((category) => {
    rows.push({
      category,
      followed: tableData[category].followed.join(', '),
      followedCount: tableData[category].followed.length,
      notFollowed: tableData[category].notFollowed.join(', '),
      notFollowedCount: tableData[category].notFollowed.length
    });
  });

  // Draw the table
  yOffset += 20;
  doc.setFontSize(10);
  doc.autoTable({
    startY: yOffset,
    head: [headers],
    body: rows.map(row => [
      row.category,
      row.followed,
      row.followedCount,
      row.notFollowed,
      row.notFollowedCount
    ]),
    margin: { left: 10, right: 10 },
    styles: {
      fontSize: 10,
      textColor: [0, 0, 0], // black text color
      lineColor: [0, 0, 0], // black border color
      lineWidth: 0.1,
    },
    headStyles: {
      fillColor: [200, 200, 200], // light gray background for header
    },
  });

  // Add Evaluation section
  doc.addPage();
  pageNumber++;
  drawFooter(doc, pageNumber, totalPages);
  doc.setFont('Arial', 'bold');
  doc.setFontSize(14);
  doc.setTextColor(0, 0, 0); // Black text color
  doc.text('Evaluation', 10, 25); // Evaluation heading outside the table
  doc.setFont('Arial', 'normal');

  apiResponse.forEach((item, index) => {
    if (index > 0) {
      doc.addPage();
      pageNumber++;
      drawFooter(doc, pageNumber, totalPages);
    }
    yOffset = 40;
    yOffset = drawQuery(doc, item, yOffset);
    drawBox(doc, yOffset);
  });

  // Save the PDF
  doc.save(`${docName}_Sustainability_Report.pdf`);
};

export const handleDownloadPDF = (analysisData) => {
  generatePDF(analysisData);
};

export default generatePDF;
