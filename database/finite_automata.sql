--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-06-26 22:45:57

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
-- TOC entry 220 (class 1259 OID 17373)
-- Name: finite_automata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.finite_automata (
    fa_id integer NOT NULL,
    name character varying(50) NOT NULL,
    fa_type character varying(3) NOT NULL,
    states text[] NOT NULL,
    alphabet text[] NOT NULL,
    start_state text NOT NULL,
    final_states text[] NOT NULL,
    user_id integer
);


ALTER TABLE public.finite_automata OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17372)
-- Name: finite_automata_fa_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.finite_automata_fa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.finite_automata_fa_id_seq OWNER TO postgres;

--
-- TOC entry 4920 (class 0 OID 0)
-- Dependencies: 219
-- Name: finite_automata_fa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.finite_automata_fa_id_seq OWNED BY public.finite_automata.fa_id;


--
-- TOC entry 222 (class 1259 OID 17401)
-- Name: transitions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transitions (
    tran_id integer NOT NULL,
    fa_id integer,
    from_state text NOT NULL,
    symbol text NOT NULL,
    to_states text[] NOT NULL
);


ALTER TABLE public.transitions OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 17400)
-- Name: transitions_tran_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transitions_tran_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transitions_tran_id_seq OWNER TO postgres;

--
-- TOC entry 4923 (class 0 OID 0)
-- Dependencies: 221
-- Name: transitions_tran_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transitions_tran_id_seq OWNED BY public.transitions.tran_id;


--
-- TOC entry 218 (class 1259 OID 17364)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password text NOT NULL,
    recovery character varying(100)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 17363)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- TOC entry 4926 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 4753 (class 2604 OID 17376)
-- Name: finite_automata fa_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.finite_automata ALTER COLUMN fa_id SET DEFAULT nextval('public.finite_automata_fa_id_seq'::regclass);


--
-- TOC entry 4754 (class 2604 OID 17404)
-- Name: transitions tran_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transitions ALTER COLUMN tran_id SET DEFAULT nextval('public.transitions_tran_id_seq'::regclass);


--
-- TOC entry 4752 (class 2604 OID 17367)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- TOC entry 4911 (class 0 OID 17373)
-- Dependencies: 220
-- Data for Name: finite_automata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.finite_automata (fa_id, name, fa_type, states, alphabet, start_state, final_states, user_id) FROM stdin;
6	End in a	DFA	{q0,q1}	{a,b}	q0	{q1}	1
7	Contain 11	NFA	{q0,q1,q2}	{0,1}	q0	{q2}	1
8	Ending in ab	NFA	{q0,q1,q2}	{a,b}	q0	{q2}	1
24	End in a Minimized	DFA	{m0,m1}	{a,b}	m1	{m0}	1
\.


--
-- TOC entry 4913 (class 0 OID 17401)
-- Dependencies: 222
-- Data for Name: transitions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transitions (tran_id, fa_id, from_state, symbol, to_states) FROM stdin;
1	6	q0	a	{q1}
2	6	q0	b	{q0}
3	6	q1	a	{q1}
4	6	q1	b	{q0}
5	7	q0	1	{q1}
6	7	q1	1	{q2}
7	7	q2	0	{q2}
8	7	q2	1	{q2}
9	8	q0	a	{q0,q1}
10	8	q0	b	{q0}
11	8	q1	b	{q2}
72	24	m0	a	{m0}
73	24	m0	b	{m1}
74	24	m1	a	{m0}
75	24	m1	b	{m1}
\.


--
-- TOC entry 4909 (class 0 OID 17364)
-- Dependencies: 218
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, username, password, recovery) FROM stdin;
1	Ririth	$2b$12$t.wNkiDU.yJwLeTLg9kCJetuL3mCk/rjOds0JK6n81y2YvaoeyVSK	ririth@member.fa.kh
\.


--
-- TOC entry 4928 (class 0 OID 0)
-- Dependencies: 219
-- Name: finite_automata_fa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.finite_automata_fa_id_seq', 24, true);


--
-- TOC entry 4929 (class 0 OID 0)
-- Dependencies: 221
-- Name: transitions_tran_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transitions_tran_id_seq', 75, true);


--
-- TOC entry 4930 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- TOC entry 4758 (class 2606 OID 17380)
-- Name: finite_automata finite_automata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.finite_automata
    ADD CONSTRAINT finite_automata_pkey PRIMARY KEY (fa_id);


--
-- TOC entry 4760 (class 2606 OID 17408)
-- Name: transitions transitions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transitions
    ADD CONSTRAINT transitions_pkey PRIMARY KEY (tran_id);


--
-- TOC entry 4756 (class 2606 OID 17371)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4761 (class 2606 OID 17381)
-- Name: finite_automata finite_automata_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.finite_automata
    ADD CONSTRAINT finite_automata_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- TOC entry 4762 (class 2606 OID 17409)
-- Name: transitions transitions_fa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transitions
    ADD CONSTRAINT transitions_fa_id_fkey FOREIGN KEY (fa_id) REFERENCES public.finite_automata(fa_id) ON DELETE CASCADE;


--
-- TOC entry 4919 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE finite_automata; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.finite_automata TO team_leader;


--
-- TOC entry 4921 (class 0 OID 0)
-- Dependencies: 219
-- Name: SEQUENCE finite_automata_fa_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.finite_automata_fa_id_seq TO team_leader;


--
-- TOC entry 4922 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE transitions; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.transitions TO team_leader;


--
-- TOC entry 4924 (class 0 OID 0)
-- Dependencies: 221
-- Name: SEQUENCE transitions_tran_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.transitions_tran_id_seq TO team_leader;


--
-- TOC entry 4925 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE users; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.users TO team_leader;


--
-- TOC entry 4927 (class 0 OID 0)
-- Dependencies: 217
-- Name: SEQUENCE users_user_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.users_user_id_seq TO team_leader;


-- Completed on 2025-06-26 22:45:57

--
-- PostgreSQL database dump complete
--

