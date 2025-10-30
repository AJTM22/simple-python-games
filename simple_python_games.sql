--
-- PostgreSQL database dump
--

\restrict S0W05zUyvOUR9ebyROKlgu1kXyhkIQw3IpoKhaX0BIsfl63uZyfetoYJmwQE71j

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2025-10-30 22:04:59

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 222 (class 1259 OID 16406)
-- Name: games; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.games (
    game_id integer NOT NULL,
    game_name text NOT NULL
);


ALTER TABLE public.games OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16405)
-- Name: games_game_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.games_game_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.games_game_id_seq OWNER TO postgres;

--
-- TOC entry 4928 (class 0 OID 0)
-- Dependencies: 221
-- Name: games_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.games_game_id_seq OWNED BY public.games.game_id;


--
-- TOC entry 223 (class 1259 OID 16418)
-- Name: player_games; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.player_games (
    player_id integer NOT NULL,
    game_id integer NOT NULL,
    best_score integer,
    latest_score integer,
    times_played integer
);


ALTER TABLE public.player_games OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16393)
-- Name: players; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.players (
    player_id integer NOT NULL,
    player_name text NOT NULL
);


ALTER TABLE public.players OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16392)
-- Name: players_player_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.players_player_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.players_player_id_seq OWNER TO postgres;

--
-- TOC entry 4929 (class 0 OID 0)
-- Dependencies: 219
-- Name: players_player_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.players_player_id_seq OWNED BY public.players.player_id;


--
-- TOC entry 4765 (class 2604 OID 16409)
-- Name: games game_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games ALTER COLUMN game_id SET DEFAULT nextval('public.games_game_id_seq'::regclass);


--
-- TOC entry 4764 (class 2604 OID 16396)
-- Name: players player_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.players ALTER COLUMN player_id SET DEFAULT nextval('public.players_player_id_seq'::regclass);


--
-- TOC entry 4771 (class 2606 OID 16417)
-- Name: games games_game_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_game_name_key UNIQUE (game_name);


--
-- TOC entry 4773 (class 2606 OID 16415)
-- Name: games games_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.games
    ADD CONSTRAINT games_pkey PRIMARY KEY (game_id);


--
-- TOC entry 4767 (class 2606 OID 16402)
-- Name: players players_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (player_id);


--
-- TOC entry 4769 (class 2606 OID 16404)
-- Name: players players_player_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT players_player_name_key UNIQUE (player_name);


--
-- TOC entry 4774 (class 2606 OID 16428)
-- Name: player_games player_games_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.player_games
    ADD CONSTRAINT player_games_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.games(game_id);


--
-- TOC entry 4775 (class 2606 OID 16423)
-- Name: player_games player_games_player_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.player_games
    ADD CONSTRAINT player_games_player_id_fkey FOREIGN KEY (player_id) REFERENCES public.players(player_id);


-- Completed on 2025-10-30 22:04:59

--
-- PostgreSQL database dump complete
--

\unrestrict S0W05zUyvOUR9ebyROKlgu1kXyhkIQw3IpoKhaX0BIsfl63uZyfetoYJmwQE71j

