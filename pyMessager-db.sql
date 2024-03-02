--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.0

-- Started on 2024-03-02 10:47:40

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 218 (class 1259 OID 24696)
-- Name: correspondences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.correspondences (
    id integer NOT NULL,
    user_id integer NOT NULL,
    user_id_with integer NOT NULL,
    user_is_read boolean,
    user_with_is_read boolean
);


ALTER TABLE public.correspondences OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24695)
-- Name: correspondences_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.correspondences_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.correspondences_id_seq OWNER TO postgres;

--
-- TOC entry 4813 (class 0 OID 0)
-- Dependencies: 217
-- Name: correspondences_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.correspondences_id_seq OWNED BY public.correspondences.id;


--
-- TOC entry 220 (class 1259 OID 24745)
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    id integer NOT NULL,
    id_sender integer NOT NULL,
    id_recipient integer NOT NULL,
    message character varying(400) NOT NULL,
    id_correspondences integer NOT NULL,
    send_time timestamp without time zone DEFAULT now(),
    is_read boolean
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24744)
-- Name: messages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.messages_id_seq OWNER TO postgres;

--
-- TOC entry 4814 (class 0 OID 0)
-- Dependencies: 219
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.messages_id_seq OWNED BY public.messages.id;


--
-- TOC entry 216 (class 1259 OID 24684)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    login character varying(100) NOT NULL,
    password character varying(100) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 24683)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4815 (class 0 OID 0)
-- Dependencies: 215
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4645 (class 2604 OID 24699)
-- Name: correspondences id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.correspondences ALTER COLUMN id SET DEFAULT nextval('public.correspondences_id_seq'::regclass);


--
-- TOC entry 4646 (class 2604 OID 24748)
-- Name: messages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages ALTER COLUMN id SET DEFAULT nextval('public.messages_id_seq'::regclass);


--
-- TOC entry 4644 (class 2604 OID 24687)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4805 (class 0 OID 24696)
-- Dependencies: 218
-- Data for Name: correspondences; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.correspondences (id, user_id, user_id_with, user_is_read, user_with_is_read) FROM stdin;
\.


--
-- TOC entry 4807 (class 0 OID 24745)
-- Dependencies: 220
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.messages (id, id_sender, id_recipient, message, id_correspondences, send_time, is_read) FROM stdin;
\.


--
-- TOC entry 4803 (class 0 OID 24684)
-- Dependencies: 216
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, login, password) FROM stdin;
\.


--
-- TOC entry 4816 (class 0 OID 0)
-- Dependencies: 217
-- Name: correspondences_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.correspondences_id_seq', 26, true);


--
-- TOC entry 4817 (class 0 OID 0)
-- Dependencies: 219
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.messages_id_seq', 40, true);


--
-- TOC entry 4818 (class 0 OID 0)
-- Dependencies: 215
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- TOC entry 4651 (class 2606 OID 24743)
-- Name: correspondences correspondences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.correspondences
    ADD CONSTRAINT correspondences_pkey PRIMARY KEY (id);


--
-- TOC entry 4653 (class 2606 OID 24750)
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- TOC entry 4649 (class 2606 OID 24689)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4656 (class 2606 OID 24761)
-- Name: messages id_correspondences; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT id_correspondences FOREIGN KEY (id_correspondences) REFERENCES public.correspondences(id);


--
-- TOC entry 4657 (class 2606 OID 24756)
-- Name: messages id_recipient; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT id_recipient FOREIGN KEY (id_recipient) REFERENCES public.users(id);


--
-- TOC entry 4658 (class 2606 OID 24751)
-- Name: messages id_sender; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT id_sender FOREIGN KEY (id_sender) REFERENCES public.users(id);


--
-- TOC entry 4654 (class 2606 OID 24700)
-- Name: correspondences user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.correspondences
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4655 (class 2606 OID 24705)
-- Name: correspondences user_id_with; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.correspondences
    ADD CONSTRAINT user_id_with FOREIGN KEY (user_id_with) REFERENCES public.users(id);


-- Completed on 2024-03-02 10:47:40

--
-- PostgreSQL database dump complete
--

