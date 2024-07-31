import * as React from 'react';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import './SampleDocumentList.css';
import NetflixFront from '../../assets/NetflixFront.jpg';
import WhatsappFront from '../../assets/WhatsappFront.jpg';
import DropboxFront from '../../assets/DropboxFront.jpg';
import InstagramFront from '../../assets/InstagramFront.jpg';
import UberFront from '../../assets/UberFront.jpg';
import { useNavigate } from "react-router-dom";

const itemData = [
  {
    img: NetflixFront,
    title: 'Netflix',
  },
  {
    img: DropboxFront,
    title: 'Dropbox',
  },
  {
    img: UberFront,
    title: 'Uber',
  },
  {
    img: InstagramFront,
    title: 'Instagram',
  },
  {
    img: WhatsappFront,
    title: 'Whatsapp',
  }
]

const SampleDocumentList = () => {
  const navigate = useNavigate();
  const handleClick = (title) => {
    navigate('/analysis', { state: { doc_name: title } });
  };


  return (
    <div className='sample-container'>
    <h4>View Results For Sample Documents</h4>
    <ImageList sx={{width: '100%', height: 250}} cols={itemData.length} rowHeight={250}>
      {itemData.map((item) => (
        <ImageListItem key={item.img}>
          <img 
            className='image'
            onClick={() => handleClick(item.title)}
            srcSet={`${item.img}?w=250&fit=crop&auto=format&dpr=2 2x`}
            src={`${item.img}?w=250&fit=crop&auto=format`}
            alt={item.title}
            loading="lazy"
          />
          <ImageListItemBar
            title={item.title}
          />
        </ImageListItem>
      ))}
    </ImageList>
    </div>
  );
};

export default SampleDocumentList;