import React, { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { Button } from "@mui/material";
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

  function createData(name, calories, fat, carbs, protein) {
    return { name, calories, fat, carbs, protein };
  }
  const rows = [
    createData("Frozen yoghurt", 159, 6.0, 24, 4.0),
    createData("Ice cream sandwich", 237, 9.0, 37, 4.3),
    createData("Eclair", 262, 16.0, 24, 6.0),
    createData("Cupcake", 305, 3.7, 67, 4.3),
    createData("Gingerbread", 356, 16.0, 49, 3.9),
  ];


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
            <TableRow>
              <TableCell sx={{ fontSize: '1.25rem' }}>Practice</TableCell>
              <TableCell sx={{ fontSize: '1.25rem' }} align="right">Query</TableCell>
              <TableCell sx={{ fontSize: '1.25rem' }} align="right">Explanation</TableCell>
              <TableCell sx={{ fontSize: '1.25rem' }} align="right">Result</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {apiRows.map((row) => (
              <TableRow
                key={row.name}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell sx={{ fontSize: '1.25rem' }} component="th" scope="row">
                  {row.practice}
                </TableCell>
                <TableCell sx={{ fontSize: '1.25rem' }} align="right">{row.query}</TableCell>
                <TableCell sx={{ fontSize: '1.25rem' }} align="right">{row.explanation}</TableCell>
                <TableCell sx={{ fontSize: '1.25rem' }} align="right">{row.result}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
