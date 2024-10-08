import jsPDF from 'jspdf';
import 'jspdf-autotable';
import gsfLogo from '../assets/GSFLogo.jpg';
import check_img from '../assets/check.jpg';
import cross_img from '../assets/cross.jpg';
import warning_img from '../assets/warning.png';
import getSampleCharts from "./chartsLoader";

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
    doc.addImage(gsfLogo, 'JPEG', 45, footerY + 2, 15, 11); // Adjust logo size and position
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
        {title: `Query ${queryNumber}:`, text: data.query},
        {title: 'Category:', text: data.category},  // Adding category information
        {title: 'Pattern:', text: data.practice},
        {title: 'If Followed:', text: data.result},
        {title: 'Suggestion:', text: data.suggestion},
        {title: 'Explanation:', text: data.explanation}
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

        // Check if the current content is "If Followed:"
        if (item.title === 'If Followed:') {
            // Calculate the xOffset for the image based on the text width
            const textWidth = doc.getTextWidth(textLines[0]);
            const imgXOffset = margin + 30 + textWidth + 5; // 5 pixels padding after text

            // Add image directly after the text with reduced size
            const imgWidth = 12;  // Adjust the width to reduce the size
            const imgHeight = 12; // Adjust the height to reduce the size
            if (item.text === "Yes") {
                doc.addImage(check_img, 'JPG', imgXOffset, yOffset - 8, imgWidth, imgHeight);
            } else if (item.text === "No") {
                doc.addImage(cross_img, 'JPG', imgXOffset, yOffset - 8, imgWidth, imgHeight);
            } else if (item.text === "Not Applicable") {
                doc.addImage(warning_img, 'PNG', imgXOffset, yOffset - 8, imgWidth, imgHeight);
            }
        }

        yOffset += lineHeight * textLines.length + 9; // Adjust space between sections
    });

    return yOffset;
};

// Function to add summary page
const addSummaryPage = (doc) => {
    const summaryText = `The EcoDoc Sense project focuses on integrating sustainability into the software design phase, aiming to assess environmental impact early on. Traditionally, sustainability is evaluated after software deployment, which can lead to inefficient designs. By considering environmental factors during design, developers can make decisions that contribute to greener software from the start.
  
    This project is motivated by the growing environmental footprint of the software industry, which is expected to significantly increase global carbon emissions. Current frameworks lack tools to evaluate sustainability based on design documents. EcoDoc Sense addresses this gap, helping developers prioritize sustainability alongside other design considerations.
  
    The methodology involves analyzing software architecture documents to rank their adherence to green patterns. These patterns are categorized into areas like resource optimization, data efficiency, performance management, security, and user impact. The project provides developers with insights to optimize designs for sustainability.
  
    To rank the documents, EcoDoc Sense uses Large Language Models (LLMs) and a structured retrieval process. The system identifies relevant green patterns in documents and generates a report based on the LLM results evaluating the design’s sustainability. This approach highlights improvement areas and guides developers in implementing sustainable patterns effectively.`;

    doc.addPage();
    doc.setFont('Arial', 'bold');
    doc.setFontSize(16);
    doc.setTextColor(0, 0, 0); // Black text color
    doc.text('About the Sustainability Report', doc.internal.pageSize.getWidth() / 2, 20, {align: 'center'});

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
    doc.text('Green patterns followed', margin, yOffset);

    yOffset += 10;
    doc.setFontSize(14);
    doc.text(`${practicesSummary.totalFollowed}/${practicesSummary.totalPractices}`, margin, yOffset);

    yOffset += 15;

    // Table headers
    doc.setFont('Arial', 'bold');
    doc.text('Categories', margin, yOffset);
    doc.text('Patterns followed', pageWidth / 2, yOffset);

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
    doc.text('Categorization of Green Patterns', pageWidth / 2, yOffset, {align: 'center'});
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
            text: 'Ensuring robust security in software prevents energy-intensive breaches or inefficiencies caused by vulnerabilities, aligning with green software patterns by maintaining system integrity without excessive resource use.'
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

const addGraphicalEvaluationPage = async (doc, docName, chartImages) => {
    let isSampleFile = ["Uber", "Instagram", "Netflix", "Dropbox", "Whatsapp"].includes(docName);
    let yOffset = 38;
    doc.addPage();

    // title
    doc.setFont('Arial', 'bold');
    doc.setFontSize(14);
    doc.setTextColor(0, 0, 0); // Black text color
    doc.text('Graphical Evaluation', 10, 20);
    doc.setFont('Arial', 'normal');

    // images
    if (isSampleFile) {
        const sampleChartsObj = getSampleCharts(docName);
        const sampleBarChart = sampleChartsObj.barChart;
        const samplePieChart = sampleChartsObj.pieChart;
        doc.addImage(sampleBarChart, 'PNG', 25, yOffset, 140, 98);
        doc.addImage(samplePieChart, 'PNG', 25, yOffset + 120, 140, 98);
    } else {
        const barChart = await fetchImageAsBase64('BarChart.png');
        const pieChart = await fetchImageAsBase64('PieChart.png');
        doc.addImage(barChart, 'PNG', 25, yOffset, 140, 98);
        doc.addImage(pieChart, 'PNG', 25, yOffset + 120, 140, 98);
    }
};
async function fetchImageAsBase64(imageName) {
    const response = await fetch(`http://localhost:8000/getImage/${imageName}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch image: ${response.statusText}`);
    }
    const blob = await response.blob();
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}

// Function to add the Improvement Plan page
const addImprovementPlanPage = (doc, apiResponse) => {
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 10;
    const boxWidth = pageWidth - 2 * margin;
    const headingHeight = 12;
    let yOffset = 25; // Initial Y offset for the first box

    // Heading for the page
    doc.addPage();  // Ensure starting on a new page
    doc.setFont('Arial', 'bold');
    doc.setFontSize(16);
    doc.setTextColor(0, 0, 0);
    doc.text('Improvement Plan', pageWidth / 2, yOffset, {align: 'center'});
    yOffset += 15; // Space after page heading

    // Calculate the number of improvements needed per category
    const improvementsSummary = {
        'Resource Optimization': [],
        'Data Efficiency': [],
        'Performance Management': [],
        'Security': [],
        'User Impact': []
    };

    apiResponse.forEach(record => {
        if (record.result === 'No' || record.result === 'Not Applicable') {
            improvementsSummary[record.category].push(record.practice);
        }
    });

    // Content for each box
    const practices = [
        {
            title: 'Resource Optimization',
            improvements: improvementsSummary['Resource Optimization'],
            count: improvementsSummary['Resource Optimization'].length
        },
        {
            title: 'Data Efficiency',
            improvements: improvementsSummary['Data Efficiency'],
            count: improvementsSummary['Data Efficiency'].length
        },
        {
            title: 'Performance Management',
            improvements: improvementsSummary['Performance Management'],
            count: improvementsSummary['Performance Management'].length
        },
        {
            title: 'Security',
            improvements: improvementsSummary['Security'],
            count: improvementsSummary['Security'].length
        },
        {
            title: 'User Impact',
            improvements: improvementsSummary['User Impact'],
            count: improvementsSummary['User Impact'].length
        }
    ];

    practices.forEach((practice) => {
        // Calculate the height needed for the box
        doc.setFont('Arial', 'normal');
        doc.setFontSize(14);
        const improvementText = practice.improvements.join("\n");
        const textLines = doc.splitTextToSize(improvementText, boxWidth - 10);
        const textHeight = textLines.length * 6;
        const boxHeight = headingHeight + textHeight + 10;

        // Check if there is enough space on the page, if not, add a new page
        if (yOffset + boxHeight > pageHeight - margin) {
            doc.addPage();
            yOffset = margin;  // Reset yOffset for the new page
        }

        // Draw the box border
        doc.setLineWidth(0.5);
        doc.rect(margin, yOffset, boxWidth, boxHeight);

        // Draw the heading row with dynamic count
        doc.setFont('Arial', 'bold');
        doc.setFontSize(14);
        doc.text(`${practice.title} - ${practice.count} improvements identified`, margin + 5, yOffset + headingHeight - 2);

        // Draw a line between the heading and content
        doc.line(margin, yOffset + headingHeight + 1, margin + boxWidth, yOffset + headingHeight + 1);

        // Draw the content row
        doc.setFont('Arial', 'normal');
        doc.setFontSize(14);
        doc.text(textLines, margin + 5, yOffset + headingHeight + 10);

        // Space after each box
        yOffset += boxHeight + 10;
    });
};

// Function to add the new "Analysis of Software Architecture Document" page
const addAnalysisPage = (doc) => {
    doc.addPage();
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 10;
    let yOffset = 25;

    // Heading for the page
    doc.setFont('Arial', 'bold');
    doc.setFontSize(16);
    doc.setTextColor(0, 0, 0);
    doc.text('Analysis of Software Architecture Document', pageWidth / 2, yOffset, {align: 'center'});

    yOffset += 20;

    // Explanation text with word wrapping
    doc.setFont('Arial', 'normal');
    doc.setFontSize(16);
    const analysisText = "The software architecture document will be evaluated based on whether it follows the mentioned green patterns or doesn't follow them or if the green patterns are not applicable for a particular document. The following symbols are used to present the final result of query:";
    const wrappedText = doc.splitTextToSize(analysisText, pageWidth - 2 * margin); // Wrap text to fit within the page width
    doc.text(wrappedText, margin, yOffset);

    yOffset += wrappedText.length * 10; // Adjust space based on the height of the wrapped text

    // Symbols explanation
    doc.addImage(check_img, 'JPG', margin, yOffset, 10, 10);
    doc.text(" - Yes, green pattern is followed", margin + 15, yOffset + 8);

    yOffset += 20;

    doc.addImage(cross_img, 'JPG', margin, yOffset, 10, 10);
    doc.text(" - No, green pattern is not followed", margin + 15, yOffset + 8);

    yOffset += 20;

    doc.addImage(warning_img, 'PNG', margin, yOffset, 10, 10);
    doc.text(" - Not applicable, green pattern is not applicable", margin + 15, yOffset + 8);
};

// Function to add table of contents page
const addTableOfContentsPage = (doc, pageNumbers) => {
    doc.addPage();
    doc.setFont('Arial', 'bold');
    doc.setFontSize(16);
    doc.setTextColor(0, 0, 0); // Black text color
    doc.text('Table of contents', doc.internal.pageSize.getWidth() / 2, 20, {align: 'center'});

    doc.setFont('Arial', 'normal');
    doc.setFontSize(14);
    doc.setTextColor(0, 0, 0); // Black text color
    const tocContent = [
        {title: 'Categorization of Green Patterns ', page: pageNumbers.greenPractices},
        {title: 'Overview', page: pageNumbers.overview},
        {title: 'Graphical Evaluation', page: pageNumbers.graphicalEvaluation},
        {title: 'Improvement Plan', page: pageNumbers.improvementPlan},
        {title: 'Analysis of Software Architecture Document', page: pageNumbers.analysisPage}, // Added the new page
        {title: 'Evaluation', page: pageNumbers.evaluation}
    ];

    tocContent.forEach((item, index) => {
        doc.text(item.title, 20, 40 + (index * 10));
        doc.text(`${item.page}`, doc.internal.pageSize.getWidth() - 20, 40 + (index * 10), {align: 'right'});
    });
};

const generatePDF = async (analysisData) => {
    const {progressValue, categoryWiseResult, apiResponse, docName, chartImages} = analysisData;
    const doc = new jsPDF();
    let pageNumber = 1;

    // Calculate total pages for footer
    const totalPages = apiResponse.length + 7; // 1 for title page, 1 for summary, 1 for table of contents, 1 for green practices, 1 for overview, 1 for graphical evaluation, 1 for improvement plan, 1 for analysis page, 1 for each query

    // Draw the title page with light leaf green background and dark green title text
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();

    // Set background color to Bright, lightest shade of green
    doc.setFillColor(255, 255, 255); // Bright, lightest shade of green
    doc.rect(0, 0, pageWidth, pageHeight, 'F'); // Fill the entire first page with light leaf green

    // Set text color for the title to dark green
    doc.setTextColor(0, 51, 51); // Dark green color
    doc.setFont('Arial', 'bold');
    doc.setFontSize(30);
    doc.text('Eco Doc Sustainability Report', pageWidth / 2, pageHeight / 2 - 10, {align: 'center'});

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
        greenPractices: summaryPageNumber + 2,
        overview: summaryPageNumber + 3,
        graphicalEvaluation: summaryPageNumber + 4,
        improvementPlan: summaryPageNumber + 5,
        analysisPage: summaryPageNumber + 6, // Adjusted page number for the new page
        evaluation: summaryPageNumber + 7
    });
    pageNumber++;
    drawFooter(doc, pageNumber, totalPages);

    // Add Green Practices for Sustainable Software page
    addGreenPracticesPage(doc);
    pageNumber++;
    drawFooter(doc, pageNumber, totalPages);

    // Dynamically calculate practices summary for the Overview page
    const practicesSummary = {
        totalFollowed: apiResponse.filter(practice => practice.result === 'Yes').length,
        totalPractices: apiResponse.length,
        data: [
            {
                pillar: 'Resource Optimization',
                followed: `${apiResponse.filter(practice => practice.category === 'Resource Optimization' && practice.result === 'Yes').length}/${apiResponse.filter(practice => practice.category === 'Resource Optimization').length}`
            },
            {
                pillar: 'Data Efficiency',
                followed: `${apiResponse.filter(practice => practice.category === 'Data Efficiency' && practice.result === 'Yes').length}/${apiResponse.filter(practice => practice.category === 'Data Efficiency').length}`
            },
            {
                pillar: 'Performance Management',
                followed: `${apiResponse.filter(practice => practice.category === 'Performance Management' && practice.result === 'Yes').length}/${apiResponse.filter(practice => practice.category === 'Performance Management').length}`
            },
            {
                pillar: 'Security',
                followed: `${apiResponse.filter(practice => practice.category === 'Security' && practice.result === 'Yes').length}/${apiResponse.filter(practice => practice.category === 'Security').length}`
            },
            {
                pillar: 'User Impact',
                followed: `${apiResponse.filter(practice => practice.category === 'User Impact' && practice.result === 'Yes').length}/${apiResponse.filter(practice => practice.category === 'User Impact').length}`
            }
        ]
    };

    // Add Overview page
    addOverviewPage(doc, practicesSummary);
    pageNumber++;
    drawFooter(doc, pageNumber, totalPages);

    // Add Graphical Evaluation
    await addGraphicalEvaluationPage(doc, docName, chartImages);
    pageNumber++;
    drawFooter(doc, pageNumber, totalPages);

    // Add Improvement Plan page
    addImprovementPlanPage(doc, apiResponse);
    pageNumber++;
    drawFooter(doc, pageNumber, totalPages);

    // Add new Analysis page
    addAnalysisPage(doc);
    pageNumber++;
    drawFooter(doc, pageNumber, totalPages);

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
        let yOffset = 40;
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
