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

  if (pageNumber > 2) { // Skip page number on the first two pages
    doc.text(`Page ${pageNumber} of ${totalPages}`, pageWidth - 30, footerY + 10); // Adjust page number position
  }
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
const drawQuery = (doc, data, yOffset, queryNumber) => {
  const pageWidth = doc.internal.pageSize.getWidth();
  const lineHeight = 10;
  const margin = 20;
  const maxWidth = pageWidth - margin * 2;

  // Define content
  const content = [
    { title: `Query ${queryNumber}:`, text: data.query },
    { title: 'Category:', text: data.category },  // Adding category information
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
    const summaryText = `The EcoDoc Sense project focuses on integrating sustainability into the software design phase, aiming to assess environmental impact early on. Traditionally, sustainability is evaluated after software deployment, which can lead to inefficient designs. By considering environmental factors during design, developers can make decisions that contribute to greener software from the start.
  
    This project is motivated by the growing environmental footprint of the software industry, which is expected to significantly increase global carbon emissions. Current frameworks lack tools to evaluate sustainability based on design documents. EcoDoc Sense addresses this gap, helping developers prioritize sustainability alongside other design considerations.
  
    The methodology involves analyzing software architecture documents to rank their adherence to green practices. These practices are categorized into areas like resource optimization, data efficiency, performance management, security, and user impact. The project provides developers with insights to optimize designs for sustainability.
  
    To rank the documents, EcoDoc Sense uses Large Language Models (LLMs) and a structured retrieval process. The system identifies relevant green practices in documents and generates a report evaluating the design’s sustainability. This approach highlights improvement areas and guides developers in implementing sustainable practices effectively.`;
  
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
  

// Function to add the Overview page
const addOverviewPage = (doc, practicesSummary) => {
  doc.addPage();
  const pageWidth = doc.internal.pageSize.getWidth();
  const margin = 10;
  let yOffset = 25;

  // Heading for the page
  doc.setFont('Arial', 'bold');
  doc.setFontSize(20);
  doc.setTextColor(0, 0, 0);
  doc.text('Overview', doc.internal.pageSize.getWidth() / 2, yOffset, { align: 'center' });

  yOffset += 15;

  // Green practices followed
  doc.setFontSize(14);
  doc.text('Green practices followed', margin, yOffset);

  yOffset += 10;
  doc.setFontSize(14);
  doc.text(`${practicesSummary.totalFollowed}/${practicesSummary.totalPractices}`, margin, yOffset);

  yOffset += 15;

  // Table headers
  doc.setFont('Arial', 'bold');
  doc.text('Categories', margin, yOffset);
  doc.text('Practices followed', pageWidth / 2, yOffset);

  yOffset += 10;

  // Table rows
  doc.setFont('Arial', 'normal');
  practicesSummary.data.forEach((item, index) => {
    doc.text(item.pillar, margin, yOffset);
    doc.text(item.followed, pageWidth / 2, yOffset);
    
    // Draw a line after each row
    if (index < practicesSummary.data.length - 1) {  // Avoid drawing line after the last row
      doc.line(margin, yOffset + 3, pageWidth - margin, yOffset + 3);
    }
    
    yOffset += 10;
  });
};

// Function to add the Green Practices for Sustainable Software page
const addGreenPracticesPage = (doc) => {
    doc.addPage();
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 10;
    const boxWidth = pageWidth - 2 * margin;
    const headingHeight = 12;
    const contentHeight = 20; // Adjusted for the new content size
    const boxHeight = headingHeight + contentHeight + 5; // Adjusted box height for both rows
    let yOffset = 25; // Initial Y offset for the first box

    // Heading for the page
    doc.setFont('Arial', 'bold');
    doc.setFontSize(16);
    doc.setTextColor(0, 0, 0);
    doc.text('Categorization of Green Practices', pageWidth / 2, yOffset, { align: 'center' });
    yOffset += 15; // Space after page heading

    // Content for each box
    const practices = [
        {
            title: 'Resource Optimization',
            text: 'This refers to using computational resources efficiently, minimizing waste, and reducing energy consumption, which is crucial in green software patterns to lower environmental impact.'
        },
        {
            title: 'Data Efficiency',
            text: 'Data efficiency focuses on minimizing the amount of data processed and stored, reducing the energy required for data handling, and contributing to the overall sustainability of software.'
        },
        {
            title: 'Performance Management',
            text: 'This involves optimizing software to perform tasks quickly and efficiently, which reduces energy usage and enhances sustainability by ensuring that resources are not unnecessarily consumed.'
        },
        {
            title: 'Security',
            text: 'Ensuring robust security in software prevents energy-intensive breaches or inefficiencies caused by vulnerabilities, aligning with green software practices by maintaining system integrity without excessive resource use.'
        },
        {
            title: 'User Impact',
            text: 'This category considers how software design affects user behavior and energy use, promoting designs that encourage energy-efficient usage patterns, thus supporting overall sustainability goals.'
        }
    ];

    // Draw each practice as a full-width box with two rows
    practices.forEach((practice) => {
        // Draw box border
        doc.setLineWidth(0.5);
        doc.rect(margin, yOffset, boxWidth, boxHeight);

        // Draw heading row
        doc.setFont('Arial', 'bold');
        doc.setFontSize(12);
        doc.text(practice.title, margin + 5, yOffset + headingHeight - 2);

        // Draw a line between the heading and content
        doc.line(margin, yOffset + headingHeight + 1, margin + boxWidth, yOffset + headingHeight + 1);

        // Draw content row
        doc.setFont('Arial', 'normal');
        doc.setFontSize(14);
        const textLines = doc.splitTextToSize(practice.text, boxWidth - 10); // Adjust text wrapping
        doc.text(textLines, margin + 5, yOffset + headingHeight + 10);

        yOffset += boxHeight + 10; // Space after each box
    });
};

// Function to add the Improvement Plan page
const addImprovementPlanPage = (doc, apiResponse) => {
    doc.addPage();
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 10;
    const boxWidth = pageWidth - 2 * margin;
    const headingHeight = 12;
    const contentHeight = 20; // Adjusted for the new content size
    const boxHeight = headingHeight + contentHeight + 5; // Adjusted box height for both rows
    let yOffset = 25; // Initial Y offset for the first box

    // Heading for the page
    doc.setFont('Arial', 'bold');
    doc.setFontSize(16);
    doc.setTextColor(0, 0, 0);
    doc.text('Improvement Plan', pageWidth / 2, yOffset, { align: 'center' });
    yOffset += 15; // Space after page heading

    // Calculate the number of improvements needed per category
    const improvementsSummary = {
        'Resource Optimization': 0,
        'Data Efficiency': 0,
        'Performance Management': 0,
        'Security': 0,
        'User Impact': 0
    };

    apiResponse.forEach(practice => {
        if (practice.result === 'No' || practice.result === 'Not Applicable') {
            improvementsSummary[practice.category] += 1;
        }
    });

    // Content for each box
    const practices = [
        { title: 'Resource Optimization', improvements: improvementsSummary['Resource Optimization'] },
        { title: 'Data Efficiency', improvements: improvementsSummary['Data Efficiency'] },
        { title: 'Performance Management', improvements: improvementsSummary['Performance Management'] },
        { title: 'Security', improvements: improvementsSummary['Security'] },
        { title: 'User Impact', improvements: improvementsSummary['User Impact'] }
    ];

    practices.forEach((practice) => {
        // Draw box border
        doc.setLineWidth(0.5);
        doc.rect(margin, yOffset, boxWidth, boxHeight);

        // Draw heading row
        doc.setFont('Arial', 'bold');
        doc.setFontSize(14);
        doc.text(practice.title, margin + 5, yOffset + headingHeight - 2);

        // Draw a line between the heading and content
        doc.line(margin, yOffset + headingHeight + 1, margin + boxWidth, yOffset + headingHeight + 1);

        // Draw content row
        doc.setFont('Arial', 'normal');
        doc.setFontSize(14);
        const improvementText = `${practice.improvements} improvements needed.`;
        const textLines = doc.splitTextToSize(improvementText, boxWidth - 10); // Adjust text wrapping
        doc.text(textLines, margin + 5, yOffset + headingHeight + 10);

        yOffset += boxHeight + 10; // Space after each box
    });
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
    { title: 'Categorization of Green Practices ', page: pageNumbers.greenPractices },
    { title: 'Overview', page: pageNumbers.overview },
    { title: 'Graphical Evaluation', page: pageNumbers.graphicalEvaluation },
    { title: 'Improvement Plan', page: pageNumbers.improvementPlan },
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
  const totalPages = apiResponse.length + 6; // 1 for title page, 1 for summary, 1 for table of contents, 1 for green practices, 1 for overview, 1 for graphical evaluation, 1 for improvement plan, 1 for ranking, and 1 for each query

  // Draw the title page with light leaf green background and dark green title text
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();

  // Set background color to Bright, lightest shade of green
  doc.setFillColor(224, 255, 224); // Bright, lightest shade of green


  doc.rect(0, 0, pageWidth, pageHeight, 'F'); // Fill the entire first page with light leaf green

  // Set text color for the title to dark green
  doc.setTextColor(0, 51, 51); // Dark green color
  doc.setFont('Arial', 'bold');
  doc.setFontSize(22);
  doc.text('Eco Doc Sustainability Report', pageWidth / 2, pageHeight / 2 - 10, { align: 'center' });

  // Add "(Generated by AI)" text in italic and bold, just below the title
  doc.setFontSize(14);
  doc.setFont('Arial', 'bolditalic'); // Set bold and italic style for the text
  doc.text('(Generated by AI)', pageWidth / 2, pageHeight / 2 + 10, { align: 'center' });

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
    greenPractices: summaryPageNumber + 1,
    overview: summaryPageNumber + 2,
    graphicalEvaluation: summaryPageNumber + 3,
    improvementPlan: summaryPageNumber + 4,
    ranking: summaryPageNumber + 5,
    evaluation: summaryPageNumber + 6
  });
  pageNumber++;
  drawFooter(doc, pageNumber, totalPages);

  // Add Green Practices for Sustainable Software page
  addGreenPracticesPage(doc);
  pageNumber++;
  drawFooter(doc, pageNumber, totalPages);

  // Add Overview page
  const practicesSummary = {
    totalFollowed: apiResponse.filter(practice => practice.result === 'Yes').length,
    totalPractices: apiResponse.length,
    data: [
      { pillar: 'Resource Optimization', followed: '5/18' },
      { pillar: 'Data Efficiency', followed: '0/5' },
      { pillar: 'Performance Management', followed: '2/8' },
      { pillar: 'Security', followed: '2/5' },
      { pillar: 'User Impact', followed: '0/1' }
    ]
  };
  addOverviewPage(doc, practicesSummary);
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

  // Add Improvement Plan page
  addImprovementPlanPage(doc, apiResponse);
  pageNumber++;
  drawFooter(doc, pageNumber, totalPages);

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
    yOffset = drawQuery(doc, item, yOffset, index + 1); // Pass the query number to drawQuery function
    drawBox(doc, yOffset);
  });

  // Save the PDF
  doc.save(`${docName}_Sustainability_Report.pdf`);
};

export const handleDownloadPDF = (analysisData) => {
  generatePDF(analysisData);
};

export default generatePDF;
