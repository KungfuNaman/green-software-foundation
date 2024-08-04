import React, { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { Button } from "@mui/material";
import { styled } from '@mui/material/styles';

export default function ResultTabs({ tabularData }) {
  const [value, setValue] = React.useState("1");
  const [apiRows,setApiRows]=useState([])
  const [listOfTabs, setListOfTabs] = useState([]);
  useEffect(() => {
    setListOfTabs(() => {
      return Object.keys(tabularData);
    });

    
  }, [tabularData]);
  const onTabClick = (event, newValue) => {
    console.log(apiRows)
    setApiRows(tabularData[newValue]);
  };
  
  const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
      backgroundColor: theme.palette.common.black,
      color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
      fontSize: 14,
    },
  }));
  
  const StyledTableRow = styled(TableRow)(({ theme }) => ({
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover,
    },
    // hide last border
    '&:last-child td, &:last-child th': {
      border: 0,
    },
  }));


  return (
    <Box sx={{ width: "100%", typography: "body1" }}>
      <div style={{display:"flex",gap:"10px",padding:"10px"}}>

      {listOfTabs.map((tab, index) => (
        <Button key={tab} variant="contained"    sx={{fontSize:'1rem'}}       onClick={(event) => onTabClick(event, tab)}
        >{tab}</Button>
      ))}
      </div>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650,fontSize: '1.25rem' }} aria-label="simple table">
          <TableHead>
            <StyledTableRow>
              <StyledTableCell sx={{ fontSize: '1.25rem' }}>Practice</StyledTableCell>
              <StyledTableCell sx={{ fontSize: '1.25rem' }} align="left">Query</StyledTableCell>
              <StyledTableCell sx={{ fontSize: '1.25rem' }} align="left">Explanation</StyledTableCell>
              <StyledTableCell sx={{ fontSize: '1.25rem' }} align="left">Result</StyledTableCell>
            </StyledTableRow>
          </TableHead>
          <TableBody>
            {apiRows.map((row) => (
              <StyledTableRow
                key={row.name}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <StyledTableCell sx={{ fontSize: '1.25rem'}} component="th" scope="row">
                  {row.practice}
                </StyledTableCell>
                <StyledTableCell sx={{ fontSize: '1.25rem'}} align="left">{row.query}</StyledTableCell>
                <StyledTableCell sx={{ fontSize: '1.25rem'}} align="left">{row.explanation}</StyledTableCell>
                <StyledTableCell sx={{ fontSize: '1.25rem'}} align="left">{row.result}</StyledTableCell>
              </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
