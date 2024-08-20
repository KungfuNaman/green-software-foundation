import InfoIcon from '@mui/icons-material/Info';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import React, {useState} from 'react';


const InformationIcon = () => {
    const [open, setOpen] = useState(false);
    const handleClickOpen = () => {
        setOpen(true);
    }
    const handleClose = () => {
        setOpen(false);
    }
    const style = {
      position: "absolute",
      top: "50%",
      left: "50%",
      transform: "translate(-50%, -50%)",
      // width: 400,
      bgcolor: "background.paper",
      // border: "2px solid #000",
      boxShadow: 24,
      maxHeight: '80vh', // Set a maximum height for the Box
      overflow:"auto",
      borderRadius:"20px",
      textAlign: 'center',
      padding : '2em',
    };


    return (
        <div>
        <InfoIcon
            sx={{
              color: '#aecc53',
              width: '20%',
              marginLeft: '11em',
              marginTop: '0.3em',
              '&:hover': {
                cursor: 'pointer',
              },
            }}
            onClick={handleClickOpen}
        />
        <Modal
            open={open}
            onClose={handleClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
          <Box sx={style}>
            <h3>Info: Progress Indicator</h3>
            <p>
               This is your progress indicator displaying real-time progress in analysing your document. Each step represents one of the 3 key steps in the pipeline.
               <ul>'Chunking Document' indicates that your document is currently being chunked, embedded and added to EcoDoc Sense's vector database. </ul>
               <ul>'Retrieving Context' indicates that EcoDoc Sense's retriever is currently fetching context from the embedded vector database and using it to create a query prompt for EcoDoc Sense's Generator LLM. </ul>
               <ul>'Generating Response' indicates that the Generator LLM is being prompted with the retrieved context and query. </ul>
               For each query, new context will be retrieved and combined with the query to create a prompt. These prompts are then iteratively presented to our generator for a response.
            </p>
          </Box>
        </Modal>
        </div>
    );
}

export default InformationIcon;