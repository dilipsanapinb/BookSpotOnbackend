
import React, { useEffect, useState } from "react";
import { Link,useNavigate } from "react-router-dom";

import Navbar from "../Components/Navbar";
import "./MoviesPage.css";
import MovieCard from "../Components/Movie/MovieCard";
import MovieFilter from "../Components/Movie/MovieFilter";
import Footer from "../Components/Footer/Footer";
// import { Carousel } from "react-responsive-carousel";
const MoviesPage = () => {


const [movies, setMovies] = useState([]);
    const [filteredMovies, setFilteredMovies] = useState(movies);

    const handleFilterChange = ({ genre, language, rating }) => {
      // Filter the movies based on the selected filters
      let filteredResult = movies;

      if (genre) {
        filteredResult = filteredResult.filter(
          (movie) => movie.genre === genre
        );
      }

      if (language) {
        filteredResult = filteredResult.filter(
          (movie) => movie.language === language
        );
      }

      if (rating) {
        const minRating = parseFloat(rating);
        filteredResult = filteredResult.filter(
          (movie) => movie.rating >= minRating
        );
      }

      setFilteredMovies(filteredResult);
    };
// Fetch movies from the API
useEffect(() => {
  fetch("http://127.0.0.1:5000/api/movies")
    .then((response) => response.json())
    .then((data) => setMovies(data))
    .catch((error) => console.error("Error fetching movies:", error));
}, []);

return (
  <div>
    <Navbar />
    <div className="movies-page-container">
      <div className="movie-filter-container">
        <MovieFilter
          genres={["Action", "Comedy", "Drama", "Adventure"]} 
          languages={["Hindi", "English", "Marathi"]} 
          onFilterChange={handleFilterChange}
        />
      </div>

      <div className="moviePge-container">
        {movies.map((movie, index) => (
          <MovieCard key={index} movie={movie} />
        ))}
      </div>
    </div>
    <Footer/>
  </div>
);
}

export default MoviesPage