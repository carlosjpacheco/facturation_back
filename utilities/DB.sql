PGDMP         *                z            invoicing_system    12.0    12.0 r    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    33382    invoicing_system    DATABASE     �   CREATE DATABASE invoicing_system WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Spanish_Venezuela.1252' LC_CTYPE = 'Spanish_Venezuela.1252';
     DROP DATABASE invoicing_system;
                postgres    false            �            1259    41588    currency    TABLE     c   CREATE TABLE public.currency (
    id integer NOT NULL,
    name character varying(10) NOT NULL
);
    DROP TABLE public.currency;
       public         heap    postgres    false            �            1259    41586    currency_id_seq    SEQUENCE     �   CREATE SEQUENCE public.currency_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.currency_id_seq;
       public          postgres    false    229            �           0    0    currency_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.currency_id_seq OWNED BY public.currency.id;
          public          postgres    false    228            �            1259    33383    detail_purchase_order    TABLE     �   CREATE TABLE public.detail_purchase_order (
    id integer NOT NULL,
    id_purchase_order bigint NOT NULL,
    products character varying[] NOT NULL,
    created_at real
);
 )   DROP TABLE public.detail_purchase_order;
       public         heap    postgres    false            �            1259    33386    detail_purchase_order_id_seq    SEQUENCE     �   CREATE SEQUENCE public.detail_purchase_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.detail_purchase_order_id_seq;
       public          postgres    false    202            �           0    0    detail_purchase_order_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.detail_purchase_order_id_seq OWNED BY public.detail_purchase_order.id;
          public          postgres    false    203            �            1259    33388    invoice_detail    TABLE     �   CREATE TABLE public.invoice_detail (
    id integer NOT NULL,
    amount character varying(50) NOT NULL,
    description character varying(100) NOT NULL,
    quantity integer NOT NULL,
    id_invoice bigint NOT NULL
);
 "   DROP TABLE public.invoice_detail;
       public         heap    postgres    false            �            1259    33391    invoice_detail_id_seq    SEQUENCE     �   CREATE SEQUENCE public.invoice_detail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.invoice_detail_id_seq;
       public          postgres    false    204            �           0    0    invoice_detail_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.invoice_detail_id_seq OWNED BY public.invoice_detail.id;
          public          postgres    false    205            �            1259    33393    invoice_payment    TABLE     �   CREATE TABLE public.invoice_payment (
    id integer NOT NULL,
    ref character varying(50) NOT NULL,
    date date NOT NULL,
    amount character varying(50) NOT NULL,
    destination character varying(100) NOT NULL,
    id_invoice bigint NOT NULL
);
 #   DROP TABLE public.invoice_payment;
       public         heap    postgres    false            �            1259    33396    invoice_payment_id_seq    SEQUENCE     �   CREATE SEQUENCE public.invoice_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.invoice_payment_id_seq;
       public          postgres    false    206            �           0    0    invoice_payment_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.invoice_payment_id_seq OWNED BY public.invoice_payment.id;
          public          postgres    false    207            �            1259    33398    invoices    TABLE     r  CREATE TABLE public.invoices (
    id integer NOT NULL,
    nro_invoice character varying(50) NOT NULL,
    id_user bigint,
    total character varying(50) NOT NULL,
    id_status bigint NOT NULL,
    id_purchase_order bigint,
    paid boolean NOT NULL,
    created_at real NOT NULL,
    deleted boolean DEFAULT true NOT NULL,
    date character varying(50) NOT NULL
);
    DROP TABLE public.invoices;
       public         heap    postgres    false            �            1259    33402    invoices_id_seq    SEQUENCE     �   CREATE SEQUENCE public.invoices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.invoices_id_seq;
       public          postgres    false    208            �           0    0    invoices_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.invoices_id_seq OWNED BY public.invoices.id;
          public          postgres    false    209            �            1259    33404    invoices_status    TABLE     k   CREATE TABLE public.invoices_status (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);
 #   DROP TABLE public.invoices_status;
       public         heap    postgres    false            �            1259    33407    invoices_status_id_seq    SEQUENCE     �   CREATE SEQUENCE public.invoices_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.invoices_status_id_seq;
       public          postgres    false    210            �           0    0    invoices_status_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.invoices_status_id_seq OWNED BY public.invoices_status.id;
          public          postgres    false    211            �            1259    33409    notifications    TABLE     �   CREATE TABLE public.notifications (
    id integer NOT NULL,
    description character varying(100) NOT NULL,
    destination bigint NOT NULL,
    read boolean NOT NULL,
    source bigint,
    date character varying NOT NULL
);
 !   DROP TABLE public.notifications;
       public         heap    postgres    false            �            1259    33415    notifications_id_seq    SEQUENCE     �   CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.notifications_id_seq;
       public          postgres    false    212            �           0    0    notifications_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;
          public          postgres    false    213            �            1259    33417    permissions    TABLE     b   CREATE TABLE public.permissions (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.permissions;
       public         heap    postgres    false            �            1259    33423    permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.permissions_id_seq;
       public          postgres    false    214            �           0    0    permissions_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;
          public          postgres    false    215            �            1259    33425    purchase_order    TABLE     K  CREATE TABLE public.purchase_order (
    id integer NOT NULL,
    id_user bigint,
    completed boolean DEFAULT false,
    deleted boolean DEFAULT true,
    id_supplier bigint NOT NULL,
    terms_conditions text,
    delivery_address text NOT NULL,
    id_currency bigint NOT NULL,
    path character varying(50),
    date real
);
 "   DROP TABLE public.purchase_order;
       public         heap    postgres    false            �            1259    33430    purchase_order_id_seq    SEQUENCE     �   CREATE SEQUENCE public.purchase_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.purchase_order_id_seq;
       public          postgres    false    216            �           0    0    purchase_order_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.purchase_order_id_seq OWNED BY public.purchase_order.id;
          public          postgres    false    217            �            1259    33432    rol_perm    TABLE     {   CREATE TABLE public.rol_perm (
    id integer NOT NULL,
    id_role bigint NOT NULL,
    id_permissions bigint NOT NULL
);
    DROP TABLE public.rol_perm;
       public         heap    postgres    false            �            1259    33435    rol_perm_id_seq    SEQUENCE     �   CREATE SEQUENCE public.rol_perm_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.rol_perm_id_seq;
       public          postgres    false    218            �           0    0    rol_perm_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.rol_perm_id_seq OWNED BY public.rol_perm.id;
          public          postgres    false    219            �            1259    33437    role    TABLE     _   CREATE TABLE public.role (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);
    DROP TABLE public.role;
       public         heap    postgres    false            �            1259    33440    role_id_seq    SEQUENCE     �   CREATE SEQUENCE public.role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.role_id_seq;
       public          postgres    false    220            �           0    0    role_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.role_id_seq OWNED BY public.role.id;
          public          postgres    false    221            �            1259    33442    status    TABLE     T   CREATE TABLE public.status (
    id integer NOT NULL,
    status bigint NOT NULL
);
    DROP TABLE public.status;
       public         heap    postgres    false            �            1259    33445    status_id_seq    SEQUENCE     �   CREATE SEQUENCE public.status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.status_id_seq;
       public          postgres    false    222            �           0    0    status_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.status_id_seq OWNED BY public.status.id;
          public          postgres    false    223            �            1259    33611    supplier_id_seq    SEQUENCE     �   CREATE SEQUENCE public.supplier_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;
 &   DROP SEQUENCE public.supplier_id_seq;
       public          postgres    false            �            1259    33613    supplier    TABLE     -  CREATE TABLE public.supplier (
    id integer DEFAULT nextval('public.supplier_id_seq'::regclass) NOT NULL,
    name character varying(100) NOT NULL,
    rif character varying(100) NOT NULL,
    fiscal_direction text NOT NULL,
    phone character varying(11) NOT NULL,
    email character varying(20) NOT NULL,
    contact_name character varying(10) NOT NULL,
    contact_lastname character varying(10) NOT NULL,
    contact_email character varying(20) NOT NULL,
    contact_phone character varying(11) NOT NULL,
    status boolean DEFAULT true NOT NULL
);
    DROP TABLE public.supplier;
       public         heap    postgres    false    226            �            1259    33452    users    TABLE     �  CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    psw character varying(100) NOT NULL,
    dni_rif character varying(100) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    id_role bigint NOT NULL,
    type_dni character varying(1) NOT NULL,
    status boolean DEFAULT true NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    33459    user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.user_id_seq;
       public          postgres    false    224            �           0    0    user_id_seq    SEQUENCE OWNED BY     <   ALTER SEQUENCE public.user_id_seq OWNED BY public.users.id;
          public          postgres    false    225            �
           2604    41591    currency id    DEFAULT     j   ALTER TABLE ONLY public.currency ALTER COLUMN id SET DEFAULT nextval('public.currency_id_seq'::regclass);
 :   ALTER TABLE public.currency ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    229    229            �
           2604    33574    detail_purchase_order id    DEFAULT     �   ALTER TABLE ONLY public.detail_purchase_order ALTER COLUMN id SET DEFAULT nextval('public.detail_purchase_order_id_seq'::regclass);
 G   ALTER TABLE public.detail_purchase_order ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    203    202            �
           2604    33575    invoice_detail id    DEFAULT     v   ALTER TABLE ONLY public.invoice_detail ALTER COLUMN id SET DEFAULT nextval('public.invoice_detail_id_seq'::regclass);
 @   ALTER TABLE public.invoice_detail ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    205    204            �
           2604    33576    invoice_payment id    DEFAULT     x   ALTER TABLE ONLY public.invoice_payment ALTER COLUMN id SET DEFAULT nextval('public.invoice_payment_id_seq'::regclass);
 A   ALTER TABLE public.invoice_payment ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    207    206            �
           2604    33577    invoices id    DEFAULT     j   ALTER TABLE ONLY public.invoices ALTER COLUMN id SET DEFAULT nextval('public.invoices_id_seq'::regclass);
 :   ALTER TABLE public.invoices ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    209    208            �
           2604    33578    invoices_status id    DEFAULT     x   ALTER TABLE ONLY public.invoices_status ALTER COLUMN id SET DEFAULT nextval('public.invoices_status_id_seq'::regclass);
 A   ALTER TABLE public.invoices_status ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    211    210            �
           2604    33579    notifications id    DEFAULT     t   ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);
 ?   ALTER TABLE public.notifications ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    213    212            �
           2604    33580    permissions id    DEFAULT     p   ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);
 =   ALTER TABLE public.permissions ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214            �
           2604    33581    purchase_order id    DEFAULT     v   ALTER TABLE ONLY public.purchase_order ALTER COLUMN id SET DEFAULT nextval('public.purchase_order_id_seq'::regclass);
 @   ALTER TABLE public.purchase_order ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216            �
           2604    33582    rol_perm id    DEFAULT     j   ALTER TABLE ONLY public.rol_perm ALTER COLUMN id SET DEFAULT nextval('public.rol_perm_id_seq'::regclass);
 :   ALTER TABLE public.rol_perm ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218            �
           2604    33583    role id    DEFAULT     b   ALTER TABLE ONLY public.role ALTER COLUMN id SET DEFAULT nextval('public.role_id_seq'::regclass);
 6   ALTER TABLE public.role ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    220            �
           2604    33584 	   status id    DEFAULT     f   ALTER TABLE ONLY public.status ALTER COLUMN id SET DEFAULT nextval('public.status_id_seq'::regclass);
 8   ALTER TABLE public.status ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    223    222            �
           2604    33586    users id    DEFAULT     c   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    225    224            �          0    41588    currency 
   TABLE DATA           ,   COPY public.currency (id, name) FROM stdin;
    public          postgres    false    229   e�       �          0    33383    detail_purchase_order 
   TABLE DATA           \   COPY public.detail_purchase_order (id, id_purchase_order, products, created_at) FROM stdin;
    public          postgres    false    202   ��       �          0    33388    invoice_detail 
   TABLE DATA           W   COPY public.invoice_detail (id, amount, description, quantity, id_invoice) FROM stdin;
    public          postgres    false    204   y�       �          0    33393    invoice_payment 
   TABLE DATA           Y   COPY public.invoice_payment (id, ref, date, amount, destination, id_invoice) FROM stdin;
    public          postgres    false    206   ��       �          0    33398    invoices 
   TABLE DATA           �   COPY public.invoices (id, nro_invoice, id_user, total, id_status, id_purchase_order, paid, created_at, deleted, date) FROM stdin;
    public          postgres    false    208   ��       �          0    33404    invoices_status 
   TABLE DATA           3   COPY public.invoices_status (id, name) FROM stdin;
    public          postgres    false    210   І       �          0    33409    notifications 
   TABLE DATA           Y   COPY public.notifications (id, description, destination, read, source, date) FROM stdin;
    public          postgres    false    212   �       �          0    33417    permissions 
   TABLE DATA           /   COPY public.permissions (id, name) FROM stdin;
    public          postgres    false    214   y�       �          0    33425    purchase_order 
   TABLE DATA           �   COPY public.purchase_order (id, id_user, completed, deleted, id_supplier, terms_conditions, delivery_address, id_currency, path, date) FROM stdin;
    public          postgres    false    216   +�       �          0    33432    rol_perm 
   TABLE DATA           ?   COPY public.rol_perm (id, id_role, id_permissions) FROM stdin;
    public          postgres    false    218   �       �          0    33437    role 
   TABLE DATA           (   COPY public.role (id, name) FROM stdin;
    public          postgres    false    220   ��       �          0    33442    status 
   TABLE DATA           ,   COPY public.status (id, status) FROM stdin;
    public          postgres    false    222   ��       �          0    33613    supplier 
   TABLE DATA           �   COPY public.supplier (id, name, rif, fiscal_direction, phone, email, contact_name, contact_lastname, contact_email, contact_phone, status) FROM stdin;
    public          postgres    false    227   �       �          0    33452    users 
   TABLE DATA           m   COPY public.users (id, username, psw, dni_rif, first_name, last_name, id_role, type_dni, status) FROM stdin;
    public          postgres    false    224   Պ       �           0    0    currency_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.currency_id_seq', 2, true);
          public          postgres    false    228            �           0    0    detail_purchase_order_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.detail_purchase_order_id_seq', 13, true);
          public          postgres    false    203            �           0    0    invoice_detail_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.invoice_detail_id_seq', 1, true);
          public          postgres    false    205            �           0    0    invoice_payment_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.invoice_payment_id_seq', 1, false);
          public          postgres    false    207            �           0    0    invoices_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.invoices_id_seq', 9, true);
          public          postgres    false    209            �           0    0    invoices_status_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.invoices_status_id_seq', 1, false);
          public          postgres    false    211            �           0    0    notifications_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.notifications_id_seq', 3, true);
          public          postgres    false    213            �           0    0    permissions_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.permissions_id_seq', 1, false);
          public          postgres    false    215            �           0    0    purchase_order_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.purchase_order_id_seq', 18, true);
          public          postgres    false    217            �           0    0    rol_perm_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.rol_perm_id_seq', 37, true);
          public          postgres    false    219            �           0    0    role_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.role_id_seq', 9, true);
          public          postgres    false    221            �           0    0    status_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.status_id_seq', 1, false);
          public          postgres    false    223            �           0    0    supplier_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.supplier_id_seq', 2, true);
          public          postgres    false    226            �           0    0    user_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.user_id_seq', 13, true);
          public          postgres    false    225                       2606    41593    currency currency_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.currency DROP CONSTRAINT currency_pkey;
       public            postgres    false    229            �
           2606    33475 0   detail_purchase_order detail_purchase_order_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.detail_purchase_order
    ADD CONSTRAINT detail_purchase_order_pkey PRIMARY KEY (id);
 Z   ALTER TABLE ONLY public.detail_purchase_order DROP CONSTRAINT detail_purchase_order_pkey;
       public            postgres    false    202            �
           2606    33621    supplier id 
   CONSTRAINT     I   ALTER TABLE ONLY public.supplier
    ADD CONSTRAINT id PRIMARY KEY (id);
 5   ALTER TABLE ONLY public.supplier DROP CONSTRAINT id;
       public            postgres    false    227            �
           2606    33479 "   invoice_detail invoice_detail_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.invoice_detail
    ADD CONSTRAINT invoice_detail_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.invoice_detail DROP CONSTRAINT invoice_detail_pkey;
       public            postgres    false    204            �
           2606    33481 $   invoice_payment invoice_payment_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.invoice_payment
    ADD CONSTRAINT invoice_payment_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.invoice_payment DROP CONSTRAINT invoice_payment_pkey;
       public            postgres    false    206            �
           2606    33483    invoices invoices_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.invoices DROP CONSTRAINT invoices_pkey;
       public            postgres    false    208            �
           2606    33485 $   invoices_status invoices_status_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.invoices_status
    ADD CONSTRAINT invoices_status_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.invoices_status DROP CONSTRAINT invoices_status_pkey;
       public            postgres    false    210            �
           2606    33487     notifications notifications_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.notifications DROP CONSTRAINT notifications_pkey;
       public            postgres    false    212            �
           2606    33489    permissions permissions_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.permissions DROP CONSTRAINT permissions_pkey;
       public            postgres    false    214            �
           2606    33491 "   purchase_order purchase_order_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT purchase_order_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.purchase_order DROP CONSTRAINT purchase_order_pkey;
       public            postgres    false    216            �
           2606    33493    rol_perm rol_perm_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.rol_perm
    ADD CONSTRAINT rol_perm_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.rol_perm DROP CONSTRAINT rol_perm_pkey;
       public            postgres    false    218            �
           2606    33495    role role_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.role DROP CONSTRAINT role_pkey;
       public            postgres    false    220            �
           2606    33497    status status_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.status DROP CONSTRAINT status_pkey;
       public            postgres    false    222            �
           2606    33499    users user_pkey 
   CONSTRAINT     M   ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);
 9   ALTER TABLE ONLY public.users DROP CONSTRAINT user_pkey;
       public            postgres    false    224                       2606    41594    purchase_order id_currency_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT id_currency_fk FOREIGN KEY (id_currency) REFERENCES public.currency(id) NOT VALID;
 G   ALTER TABLE ONLY public.purchase_order DROP CONSTRAINT id_currency_fk;
       public          postgres    false    2817    216    229                       2606    33505    notifications id_destination_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT id_destination_fk FOREIGN KEY (destination) REFERENCES public.users(id) NOT VALID;
 I   ALTER TABLE ONLY public.notifications DROP CONSTRAINT id_destination_fk;
       public          postgres    false    224    2813    212                       2606    33510    invoice_detail id_invoice_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.invoice_detail
    ADD CONSTRAINT id_invoice_fk FOREIGN KEY (id_invoice) REFERENCES public.invoices(id);
 F   ALTER TABLE ONLY public.invoice_detail DROP CONSTRAINT id_invoice_fk;
       public          postgres    false    208    204    2797                       2606    33515    invoice_payment id_invoice_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.invoice_payment
    ADD CONSTRAINT id_invoice_fk FOREIGN KEY (id_invoice) REFERENCES public.invoices(id);
 G   ALTER TABLE ONLY public.invoice_payment DROP CONSTRAINT id_invoice_fk;
       public          postgres    false    208    206    2797                       2606    33589    invoices id_invoice_status    FK CONSTRAINT     �   ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT id_invoice_status FOREIGN KEY (id_status) REFERENCES public.invoices_status(id) NOT VALID;
 D   ALTER TABLE ONLY public.invoices DROP CONSTRAINT id_invoice_status;
       public          postgres    false    208    210    2799                       2606    33520    rol_perm id_permissions    FK CONSTRAINT     �   ALTER TABLE ONLY public.rol_perm
    ADD CONSTRAINT id_permissions FOREIGN KEY (id_permissions) REFERENCES public.permissions(id) NOT VALID;
 A   ALTER TABLE ONLY public.rol_perm DROP CONSTRAINT id_permissions;
       public          postgres    false    218    2803    214                       2606    33525 *   detail_purchase_order id_purchase_order_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_purchase_order
    ADD CONSTRAINT id_purchase_order_fk FOREIGN KEY (id_purchase_order) REFERENCES public.purchase_order(id) NOT VALID;
 T   ALTER TABLE ONLY public.detail_purchase_order DROP CONSTRAINT id_purchase_order_fk;
       public          postgres    false    2805    216    202                       2606    33530    invoices id_purchase_order_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT id_purchase_order_fk FOREIGN KEY (id_purchase_order) REFERENCES public.purchase_order(id);
 G   ALTER TABLE ONLY public.invoices DROP CONSTRAINT id_purchase_order_fk;
       public          postgres    false    208    2805    216                       2606    33535    rol_perm id_role    FK CONSTRAINT     x   ALTER TABLE ONLY public.rol_perm
    ADD CONSTRAINT id_role FOREIGN KEY (id_role) REFERENCES public.role(id) NOT VALID;
 :   ALTER TABLE ONLY public.rol_perm DROP CONSTRAINT id_role;
       public          postgres    false    218    220    2809                       2606    33540    users id_role_fk    FK CONSTRAINT     x   ALTER TABLE ONLY public.users
    ADD CONSTRAINT id_role_fk FOREIGN KEY (id_role) REFERENCES public.role(id) NOT VALID;
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT id_role_fk;
       public          postgres    false    2809    224    220            	           2606    33545    notifications id_source_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT id_source_fk FOREIGN KEY (source) REFERENCES public.users(id) NOT VALID;
 D   ALTER TABLE ONLY public.notifications DROP CONSTRAINT id_source_fk;
       public          postgres    false    2813    212    224                       2606    41574    purchase_order id_supplier_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT id_supplier_fk FOREIGN KEY (id_supplier) REFERENCES public.supplier(id) NOT VALID;
 G   ALTER TABLE ONLY public.purchase_order DROP CONSTRAINT id_supplier_fk;
       public          postgres    false    216    227    2815            
           2606    33555    purchase_order id_user_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT id_user_fk FOREIGN KEY (id_user) REFERENCES public.users(id) NOT VALID;
 C   ALTER TABLE ONLY public.purchase_order DROP CONSTRAINT id_user_fk;
       public          postgres    false    224    216    2813                       2606    41602    invoices id_user_fk    FK CONSTRAINT     |   ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT id_user_fk FOREIGN KEY (id_user) REFERENCES public.users(id) NOT VALID;
 =   ALTER TABLE ONLY public.invoices DROP CONSTRAINT id_user_fk;
       public          postgres    false    2813    208    224            �   "   x�3�t��9��,�(��ː����03F��� ��	�      �   �   x�e�=�0���+�%CE�h�����H�v	D�D�"��^��,Y��}�.%�q�w=t���j���0M��� �T�����.]e�^�F#\J��g��pN�Y��m�[��Go�q��lF���২z��Ar�#��"��J�FJ��z�,\�%x~�J),�H����tOZj�>Dm��V�Ŋdˁ��Z�Uϱص�s��N�g�8����^.      �      x������ � �      �      x������ � �      �      x������ � �      �   "   x�3�ptwtq�2�p�s�t�q����� L�j      �   g   x���1�0��>�O�ǉ��љ%�A�@����gd�<�Ds[��6��U�ٮ*c_[���2^ｒӓ&�eM���-��e5Fd��e�d��[�%��=0�l]2�      �   �   x�]�=�0���>LE(�c�Q	HQ$��C:��-C��q�~��$C���1�0���;�tZ�Wac�:�Xf+�l��߻6�x=��|=vq�z������'Sĉ$F���1��k���ڙM{�j]T�Ħ�vZ�G�y�l�3Z8���#�<��7D�����      �   �   x�]�A� �~
���Mw�u����xЂ�rí}�����������X���j����'c����z�|�*P�<�|oTV�z�
���
5���	����n�����w��h�&,�.��8,q�R:����_M@j2:[�'d7R�8��&�K�B<	:��۶��m@���� ��\�      �   �   x���0k1L�A�������N,�T*���t6�sb;�s�:����@f7���`����޿j{5\��j�z��ݚ�-ׁ��B�������c|8�w@�wH�wP�wX���Y<蝾�S+����$E      �   ]   x���L�-�IML��2�tO-J�+IUHIUpL����,.)JL�<�9�˘�1/1(��M֐!��_�e�l�s~^IbRfNfJb
�)�9(R1z\\\ w�1�      �      x�3�4�2�4������ ��      �   �   x�}���0�s�> ����"F=zi�����d��@C<yi��E����t�Ȱ�r�E�f;R����L֚�SHҺ*Ӑ�!��A��ː��H�1\o��H�C���((pYKab1\d�e��(��������ЏZ:��:k@���>_��'�����7�'FN      �   �  x���M�1F��S�A���r����@�@!�R�j�C�=�������d#i!����*o�zz���$D����Ւ�*k�N�S�� )Z�2���h�>�O!S�o��3��u��,��
��Cr�C���6��Y�޷��Gs�qEs�R��BNTH9��-` KH�'x���t���໧��O\3�嚥 s�[K�&�{���HN�\(R�%ꑼH��g.�p
��Cnз��/��/2�#���m=��=����x�E/k!#�����D�`��Drh�"b����9�F��
���Qg̥�B��4�^u���a�"|_������f��y=)��2�]�G�2��~���%2K��M�RJ-J�*<��d\��zk[����I6�T�<�k����V=>����|hW�[����v�?�5��     