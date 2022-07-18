PGDMP         )                z            invoicing_system    12.0    12.0 �    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
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
       public          postgres    false    227            �           0    0    currency_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.currency_id_seq OWNED BY public.currency.id;
          public          postgres    false    226            �            1259    33383    detail_purchase_order    TABLE     �   CREATE TABLE public.detail_purchase_order (
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
          public          postgres    false    205            �            1259    41637    invoice_detail_robot_id_seq    SEQUENCE     �   CREATE SEQUENCE public.invoice_detail_robot_id_seq
    START WITH 7
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;
 2   DROP SEQUENCE public.invoice_detail_robot_id_seq;
       public          postgres    false            �            1259    41639    invoice_detail_robot    TABLE       CREATE TABLE public.invoice_detail_robot (
    id integer DEFAULT nextval('public.invoice_detail_robot_id_seq'::regclass) NOT NULL,
    amount character varying(50),
    description character varying(100),
    id_invoice bigint NOT NULL,
    quantity character varying(10)
);
 (   DROP TABLE public.invoice_detail_robot;
       public         heap    postgres    false    232            �            1259    41658    invoice_items    TABLE     o   CREATE TABLE public.invoice_items (
    id integer NOT NULL,
    item character varying,
    status boolean
);
 !   DROP TABLE public.invoice_items;
       public         heap    postgres    false            �            1259    41656    invoice_items_id_seq    SEQUENCE     �   CREATE SEQUENCE public.invoice_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.invoice_items_id_seq;
       public          postgres    false    235            �           0    0    invoice_items_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.invoice_items_id_seq OWNED BY public.invoice_items.id;
          public          postgres    false    234            �            1259    33398    invoices    TABLE     c  CREATE TABLE public.invoices (
    id integer NOT NULL,
    nro_invoice character varying(50) NOT NULL,
    id_user bigint,
    id_status bigint NOT NULL,
    id_purchase_order bigint NOT NULL,
    paid boolean NOT NULL,
    created_at real,
    deleted boolean DEFAULT true NOT NULL,
    date character varying(50) NOT NULL,
    name_supplier character varying(50),
    paid_at real,
    total real,
    path character varying(50),
    shipping_address character varying,
    tax character varying,
    payment_terms character varying,
    currency character varying,
    shipping_charges character varying
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
       public          postgres    false    206            �           0    0    invoices_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.invoices_id_seq OWNED BY public.invoices.id;
          public          postgres    false    207            �            1259    41625    invoices_robot_id_seq    SEQUENCE     �   CREATE SEQUENCE public.invoices_robot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;
 ,   DROP SEQUENCE public.invoices_robot_id_seq;
       public          postgres    false            �            1259    41631    invoices_robot    TABLE     �  CREATE TABLE public.invoices_robot (
    id integer DEFAULT nextval('public.invoices_robot_id_seq'::regclass) NOT NULL,
    nro_invoice character varying(50),
    total character varying(50),
    date character varying(50),
    name_supplier character varying(50),
    path character varying(50) NOT NULL,
    shipping_address character varying(100),
    tax character varying(50),
    payment_terms character varying(100),
    currency character varying(50),
    shipping_charges character varying(100)
);
 "   DROP TABLE public.invoices_robot;
       public         heap    postgres    false    230            �            1259    33404    invoices_status    TABLE     k   CREATE TABLE public.invoices_status (
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
       public          postgres    false    208            �           0    0    invoices_status_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.invoices_status_id_seq OWNED BY public.invoices_status.id;
          public          postgres    false    209            �            1259    33409    notifications    TABLE     �   CREATE TABLE public.notifications (
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
       public          postgres    false    210            �           0    0    notifications_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;
          public          postgres    false    211            �            1259    41609    operation_history    TABLE     �   CREATE TABLE public.operation_history (
    id integer NOT NULL,
    description character varying(100) NOT NULL,
    id_user bigint NOT NULL,
    date timestamp without time zone NOT NULL
);
 %   DROP TABLE public.operation_history;
       public         heap    postgres    false            �            1259    41607    operation_history_id_seq    SEQUENCE     �   CREATE SEQUENCE public.operation_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.operation_history_id_seq;
       public          postgres    false    229            �           0    0    operation_history_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.operation_history_id_seq OWNED BY public.operation_history.id;
          public          postgres    false    228            �            1259    33417    permissions    TABLE     b   CREATE TABLE public.permissions (
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
       public          postgres    false    212            �           0    0    permissions_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;
          public          postgres    false    213            �            1259    33425    purchase_order    TABLE     b  CREATE TABLE public.purchase_order (
    id integer NOT NULL,
    id_user bigint,
    completed boolean DEFAULT false,
    deleted boolean DEFAULT true,
    id_supplier bigint NOT NULL,
    terms_conditions text,
    delivery_address text NOT NULL,
    id_currency bigint NOT NULL,
    path character varying(50),
    date real,
    completed_at real
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
       public          postgres    false    214            �           0    0    purchase_order_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.purchase_order_id_seq OWNED BY public.purchase_order.id;
          public          postgres    false    215            �            1259    33432    rol_perm    TABLE     {   CREATE TABLE public.rol_perm (
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
       public          postgres    false    216            �           0    0    rol_perm_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.rol_perm_id_seq OWNED BY public.rol_perm.id;
          public          postgres    false    217            �            1259    33437    role    TABLE     _   CREATE TABLE public.role (
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
       public          postgres    false    218            �           0    0    role_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.role_id_seq OWNED BY public.role.id;
          public          postgres    false    219            �            1259    33442    status    TABLE     T   CREATE TABLE public.status (
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
       public          postgres    false    220            �           0    0    status_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.status_id_seq OWNED BY public.status.id;
          public          postgres    false    221            �            1259    33611    supplier_id_seq    SEQUENCE     �   CREATE SEQUENCE public.supplier_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;
 &   DROP SEQUENCE public.supplier_id_seq;
       public          postgres    false            �            1259    33613    supplier    TABLE     1  CREATE TABLE public.supplier (
    id integer DEFAULT nextval('public.supplier_id_seq'::regclass) NOT NULL,
    name character varying(100) NOT NULL,
    rif character varying(100) NOT NULL,
    fiscal_direction text NOT NULL,
    phone character varying(11) NOT NULL,
    email character varying(100) NOT NULL,
    contact_name character varying(100) NOT NULL,
    contact_lastname character varying(100) NOT NULL,
    contact_email character varying(100) NOT NULL,
    contact_phone character varying(11) NOT NULL,
    status boolean DEFAULT true NOT NULL
);
    DROP TABLE public.supplier;
       public         heap    postgres    false    224            �            1259    33452    users    TABLE     �  CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    psw character varying(100) NOT NULL,
    dni_rif character varying(100) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    id_role bigint NOT NULL,
    type_dni character varying(1) NOT NULL,
    status boolean DEFAULT true NOT NULL,
    email character varying,
    attemp bigint
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
       public          postgres    false    222            �           0    0    user_id_seq    SEQUENCE OWNED BY     <   ALTER SEQUENCE public.user_id_seq OWNED BY public.users.id;
          public          postgres    false    223            �
           2604    41591    currency id    DEFAULT     j   ALTER TABLE ONLY public.currency ALTER COLUMN id SET DEFAULT nextval('public.currency_id_seq'::regclass);
 :   ALTER TABLE public.currency ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    226    227    227            �
           2604    33574    detail_purchase_order id    DEFAULT     �   ALTER TABLE ONLY public.detail_purchase_order ALTER COLUMN id SET DEFAULT nextval('public.detail_purchase_order_id_seq'::regclass);
 G   ALTER TABLE public.detail_purchase_order ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    203    202            �
           2604    33575    invoice_detail id    DEFAULT     v   ALTER TABLE ONLY public.invoice_detail ALTER COLUMN id SET DEFAULT nextval('public.invoice_detail_id_seq'::regclass);
 @   ALTER TABLE public.invoice_detail ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    205    204            �
           2604    41661    invoice_items id    DEFAULT     t   ALTER TABLE ONLY public.invoice_items ALTER COLUMN id SET DEFAULT nextval('public.invoice_items_id_seq'::regclass);
 ?   ALTER TABLE public.invoice_items ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    234    235    235            �
           2604    33577    invoices id    DEFAULT     j   ALTER TABLE ONLY public.invoices ALTER COLUMN id SET DEFAULT nextval('public.invoices_id_seq'::regclass);
 :   ALTER TABLE public.invoices ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    207    206            �
           2604    33578    invoices_status id    DEFAULT     x   ALTER TABLE ONLY public.invoices_status ALTER COLUMN id SET DEFAULT nextval('public.invoices_status_id_seq'::regclass);
 A   ALTER TABLE public.invoices_status ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    209    208            �
           2604    33579    notifications id    DEFAULT     t   ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);
 ?   ALTER TABLE public.notifications ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    211    210            �
           2604    41612    operation_history id    DEFAULT     |   ALTER TABLE ONLY public.operation_history ALTER COLUMN id SET DEFAULT nextval('public.operation_history_id_seq'::regclass);
 C   ALTER TABLE public.operation_history ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    229    229            �
           2604    33580    permissions id    DEFAULT     p   ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);
 =   ALTER TABLE public.permissions ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    213    212            �
           2604    33581    purchase_order id    DEFAULT     v   ALTER TABLE ONLY public.purchase_order ALTER COLUMN id SET DEFAULT nextval('public.purchase_order_id_seq'::regclass);
 @   ALTER TABLE public.purchase_order ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214            �
           2604    33582    rol_perm id    DEFAULT     j   ALTER TABLE ONLY public.rol_perm ALTER COLUMN id SET DEFAULT nextval('public.rol_perm_id_seq'::regclass);
 :   ALTER TABLE public.rol_perm ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216            �
           2604    33583    role id    DEFAULT     b   ALTER TABLE ONLY public.role ALTER COLUMN id SET DEFAULT nextval('public.role_id_seq'::regclass);
 6   ALTER TABLE public.role ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218            �
           2604    33584 	   status id    DEFAULT     f   ALTER TABLE ONLY public.status ALTER COLUMN id SET DEFAULT nextval('public.status_id_seq'::regclass);
 8   ALTER TABLE public.status ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    220            �
           2604    33586    users id    DEFAULT     c   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    223    222            �          0    41588    currency 
   TABLE DATA           ,   COPY public.currency (id, name) FROM stdin;
    public          postgres    false    227   %�       �          0    33383    detail_purchase_order 
   TABLE DATA           \   COPY public.detail_purchase_order (id, id_purchase_order, products, created_at) FROM stdin;
    public          postgres    false    202   W�       �          0    33388    invoice_detail 
   TABLE DATA           W   COPY public.invoice_detail (id, amount, description, quantity, id_invoice) FROM stdin;
    public          postgres    false    204   �       �          0    41639    invoice_detail_robot 
   TABLE DATA           ]   COPY public.invoice_detail_robot (id, amount, description, id_invoice, quantity) FROM stdin;
    public          postgres    false    233   ��       �          0    41658    invoice_items 
   TABLE DATA           9   COPY public.invoice_items (id, item, status) FROM stdin;
    public          postgres    false    235   ��       �          0    33398    invoices 
   TABLE DATA           �   COPY public.invoices (id, nro_invoice, id_user, id_status, id_purchase_order, paid, created_at, deleted, date, name_supplier, paid_at, total, path, shipping_address, tax, payment_terms, currency, shipping_charges) FROM stdin;
    public          postgres    false    206   K�       �          0    41631    invoices_robot 
   TABLE DATA           �   COPY public.invoices_robot (id, nro_invoice, total, date, name_supplier, path, shipping_address, tax, payment_terms, currency, shipping_charges) FROM stdin;
    public          postgres    false    231   �       �          0    33404    invoices_status 
   TABLE DATA           3   COPY public.invoices_status (id, name) FROM stdin;
    public          postgres    false    208   1�       �          0    33409    notifications 
   TABLE DATA           Y   COPY public.notifications (id, description, destination, read, source, date) FROM stdin;
    public          postgres    false    210   m�       �          0    41609    operation_history 
   TABLE DATA           K   COPY public.operation_history (id, description, id_user, date) FROM stdin;
    public          postgres    false    229   �       �          0    33417    permissions 
   TABLE DATA           /   COPY public.permissions (id, name) FROM stdin;
    public          postgres    false    212   <�       �          0    33425    purchase_order 
   TABLE DATA           �   COPY public.purchase_order (id, id_user, completed, deleted, id_supplier, terms_conditions, delivery_address, id_currency, path, date, completed_at) FROM stdin;
    public          postgres    false    214   �       �          0    33432    rol_perm 
   TABLE DATA           ?   COPY public.rol_perm (id, id_role, id_permissions) FROM stdin;
    public          postgres    false    216   ��       �          0    33437    role 
   TABLE DATA           (   COPY public.role (id, name) FROM stdin;
    public          postgres    false    218   J�       �          0    33442    status 
   TABLE DATA           ,   COPY public.status (id, status) FROM stdin;
    public          postgres    false    220   ��       �          0    33613    supplier 
   TABLE DATA           �   COPY public.supplier (id, name, rif, fiscal_direction, phone, email, contact_name, contact_lastname, contact_email, contact_phone, status) FROM stdin;
    public          postgres    false    225   ܥ       �          0    33452    users 
   TABLE DATA           |   COPY public.users (id, username, psw, dni_rif, first_name, last_name, id_role, type_dni, status, email, attemp) FROM stdin;
    public          postgres    false    222   \�       �           0    0    currency_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.currency_id_seq', 2, true);
          public          postgres    false    226            �           0    0    detail_purchase_order_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.detail_purchase_order_id_seq', 39, true);
          public          postgres    false    203            �           0    0    invoice_detail_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.invoice_detail_id_seq', 59, true);
          public          postgres    false    205            �           0    0    invoice_detail_robot_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.invoice_detail_robot_id_seq', 218, true);
          public          postgres    false    232            �           0    0    invoice_items_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.invoice_items_id_seq', 9, true);
          public          postgres    false    234            �           0    0    invoices_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.invoices_id_seq', 53, true);
          public          postgres    false    207            �           0    0    invoices_robot_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.invoices_robot_id_seq', 87, true);
          public          postgres    false    230            �           0    0    invoices_status_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.invoices_status_id_seq', 1, false);
          public          postgres    false    209            �           0    0    notifications_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.notifications_id_seq', 76, true);
          public          postgres    false    211            �           0    0    operation_history_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.operation_history_id_seq', 147, true);
          public          postgres    false    228            �           0    0    permissions_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.permissions_id_seq', 1, false);
          public          postgres    false    213            �           0    0    purchase_order_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.purchase_order_id_seq', 51, true);
          public          postgres    false    215            �           0    0    rol_perm_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.rol_perm_id_seq', 37, true);
          public          postgres    false    217            �           0    0    role_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.role_id_seq', 10, true);
          public          postgres    false    219            �           0    0    status_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.status_id_seq', 1, false);
          public          postgres    false    221            �           0    0    supplier_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.supplier_id_seq', 23, true);
          public          postgres    false    224            �           0    0    user_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.user_id_seq', 46, true);
          public          postgres    false    223                       2606    41593    currency currency_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.currency DROP CONSTRAINT currency_pkey;
       public            postgres    false    227            �
           2606    33475 0   detail_purchase_order detail_purchase_order_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.detail_purchase_order
    ADD CONSTRAINT detail_purchase_order_pkey PRIMARY KEY (id);
 Z   ALTER TABLE ONLY public.detail_purchase_order DROP CONSTRAINT detail_purchase_order_pkey;
       public            postgres    false    202                       2606    33621    supplier id 
   CONSTRAINT     I   ALTER TABLE ONLY public.supplier
    ADD CONSTRAINT id PRIMARY KEY (id);
 5   ALTER TABLE ONLY public.supplier DROP CONSTRAINT id;
       public            postgres    false    225                       2606    33479 "   invoice_detail invoice_detail_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.invoice_detail
    ADD CONSTRAINT invoice_detail_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.invoice_detail DROP CONSTRAINT invoice_detail_pkey;
       public            postgres    false    204                       2606    41644 .   invoice_detail_robot invoice_detail_robot_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.invoice_detail_robot
    ADD CONSTRAINT invoice_detail_robot_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.invoice_detail_robot DROP CONSTRAINT invoice_detail_robot_pkey;
       public            postgres    false    233                       2606    41666     invoice_items invoice_items_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.invoice_items
    ADD CONSTRAINT invoice_items_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.invoice_items DROP CONSTRAINT invoice_items_pkey;
       public            postgres    false    235                       2606    33483    invoices invoices_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.invoices DROP CONSTRAINT invoices_pkey;
       public            postgres    false    206                       2606    41636 "   invoices_robot invoices_robot_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.invoices_robot
    ADD CONSTRAINT invoices_robot_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.invoices_robot DROP CONSTRAINT invoices_robot_pkey;
       public            postgres    false    231                       2606    33485 $   invoices_status invoices_status_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.invoices_status
    ADD CONSTRAINT invoices_status_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.invoices_status DROP CONSTRAINT invoices_status_pkey;
       public            postgres    false    208                       2606    33487     notifications notifications_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.notifications DROP CONSTRAINT notifications_pkey;
       public            postgres    false    210                       2606    41614 (   operation_history operation_history_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.operation_history
    ADD CONSTRAINT operation_history_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.operation_history DROP CONSTRAINT operation_history_pkey;
       public            postgres    false    229            	           2606    33489    permissions permissions_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.permissions DROP CONSTRAINT permissions_pkey;
       public            postgres    false    212                       2606    33491 "   purchase_order purchase_order_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT purchase_order_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.purchase_order DROP CONSTRAINT purchase_order_pkey;
       public            postgres    false    214                       2606    33493    rol_perm rol_perm_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.rol_perm
    ADD CONSTRAINT rol_perm_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.rol_perm DROP CONSTRAINT rol_perm_pkey;
       public            postgres    false    216                       2606    33495    role role_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.role DROP CONSTRAINT role_pkey;
       public            postgres    false    218                       2606    33497    status status_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.status DROP CONSTRAINT status_pkey;
       public            postgres    false    220                       2606    33499    users user_pkey 
   CONSTRAINT     M   ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);
 9   ALTER TABLE ONLY public.users DROP CONSTRAINT user_pkey;
       public            postgres    false    222            )           2606    41594    purchase_order id_currency_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT id_currency_fk FOREIGN KEY (id_currency) REFERENCES public.currency(id) NOT VALID;
 G   ALTER TABLE ONLY public.purchase_order DROP CONSTRAINT id_currency_fk;
       public          postgres    false    227    2839    214            %           2606    33505    notifications id_destination_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT id_destination_fk FOREIGN KEY (destination) REFERENCES public.users(id) NOT VALID;
 I   ALTER TABLE ONLY public.notifications DROP CONSTRAINT id_destination_fk;
       public          postgres    false    210    2835    222            !           2606    33510    invoice_detail id_invoice_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.invoice_detail
    ADD CONSTRAINT id_invoice_fk FOREIGN KEY (id_invoice) REFERENCES public.invoices(id);
 F   ALTER TABLE ONLY public.invoice_detail DROP CONSTRAINT id_invoice_fk;
       public          postgres    false    2819    206    204            .           2606    41645 (   invoice_detail_robot id_invoice_robot_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.invoice_detail_robot
    ADD CONSTRAINT id_invoice_robot_fk FOREIGN KEY (id_invoice) REFERENCES public.invoices_robot(id);
 R   ALTER TABLE ONLY public.invoice_detail_robot DROP CONSTRAINT id_invoice_robot_fk;
       public          postgres    false    231    2843    233            #           2606    33589    invoices id_invoice_status    FK CONSTRAINT     �   ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT id_invoice_status FOREIGN KEY (id_status) REFERENCES public.invoices_status(id) NOT VALID;
 D   ALTER TABLE ONLY public.invoices DROP CONSTRAINT id_invoice_status;
       public          postgres    false    2821    208    206            *           2606    33520    rol_perm id_permissions    FK CONSTRAINT     �   ALTER TABLE ONLY public.rol_perm
    ADD CONSTRAINT id_permissions FOREIGN KEY (id_permissions) REFERENCES public.permissions(id) NOT VALID;
 A   ALTER TABLE ONLY public.rol_perm DROP CONSTRAINT id_permissions;
       public          postgres    false    212    216    2825                        2606    33525 *   detail_purchase_order id_purchase_order_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_purchase_order
    ADD CONSTRAINT id_purchase_order_fk FOREIGN KEY (id_purchase_order) REFERENCES public.purchase_order(id) NOT VALID;
 T   ALTER TABLE ONLY public.detail_purchase_order DROP CONSTRAINT id_purchase_order_fk;
       public          postgres    false    214    202    2827            "           2606    33530    invoices id_purchase_order_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT id_purchase_order_fk FOREIGN KEY (id_purchase_order) REFERENCES public.purchase_order(id);
 G   ALTER TABLE ONLY public.invoices DROP CONSTRAINT id_purchase_order_fk;
       public          postgres    false    214    2827    206            +           2606    33535    rol_perm id_role    FK CONSTRAINT     x   ALTER TABLE ONLY public.rol_perm
    ADD CONSTRAINT id_role FOREIGN KEY (id_role) REFERENCES public.role(id) NOT VALID;
 :   ALTER TABLE ONLY public.rol_perm DROP CONSTRAINT id_role;
       public          postgres    false    2831    218    216            ,           2606    33540    users id_role_fk    FK CONSTRAINT     x   ALTER TABLE ONLY public.users
    ADD CONSTRAINT id_role_fk FOREIGN KEY (id_role) REFERENCES public.role(id) NOT VALID;
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT id_role_fk;
       public          postgres    false    2831    218    222            &           2606    33545    notifications id_source_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT id_source_fk FOREIGN KEY (source) REFERENCES public.users(id) NOT VALID;
 D   ALTER TABLE ONLY public.notifications DROP CONSTRAINT id_source_fk;
       public          postgres    false    2835    222    210            (           2606    41574    purchase_order id_supplier_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT id_supplier_fk FOREIGN KEY (id_supplier) REFERENCES public.supplier(id) NOT VALID;
 G   ALTER TABLE ONLY public.purchase_order DROP CONSTRAINT id_supplier_fk;
       public          postgres    false    2837    214    225            '           2606    33555    purchase_order id_user_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT id_user_fk FOREIGN KEY (id_user) REFERENCES public.users(id) NOT VALID;
 C   ALTER TABLE ONLY public.purchase_order DROP CONSTRAINT id_user_fk;
       public          postgres    false    222    214    2835            $           2606    41602    invoices id_user_fk    FK CONSTRAINT     |   ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT id_user_fk FOREIGN KEY (id_user) REFERENCES public.users(id) NOT VALID;
 =   ALTER TABLE ONLY public.invoices DROP CONSTRAINT id_user_fk;
       public          postgres    false    206    222    2835            -           2606    41620    operation_history id_user_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.operation_history
    ADD CONSTRAINT id_user_fk FOREIGN KEY (id_user) REFERENCES public.users(id) NOT VALID;
 F   ALTER TABLE ONLY public.operation_history DROP CONSTRAINT id_user_fk;
       public          postgres    false    229    2835    222            �   "   x�3�t��9��,�(��ː����03F��� ��	�      �   �   x�M���0E��+K56��:*W���HA¿�J����{�I2thY�^�"�T���&+���X5�CYz\WĢ��,�Bb�������κѮ���*���'F�@B�<����p`��KӸ���S �<����m�	9��o�u�+��Tga���R�!="���]@"      �   h   x�35�460�30��I,(�/V��4�45�25�42K����$4��s��RӋ�59M��,8-�|R����9�9M��L-9-�Ry�%�E`38�@R1z\\\ 6�      �      x������ � �      �   �   x�=�;�0D��)|$�P��H�f�7�R�q%�Tt�����������	$��mzBR8��UZB��*T|��ȱ��	�B[0�%�G�ח;�Vm���#�<a�;8s$WqG/d���X�<��(���_^fJ�/V7�      �   �   x�]��
�@��w�b�1Ý;�f;� ���*�H� �#j�T=E/�?�
��p9���B��
��
���V�Dv��	��1C�-'�
���g�[���1֮x��\߹���I>���v��8gW��q%�� ex�~ 34y&XE��KD���?������i�>�g��b�"�V��~8aY.c��;�      �      x������ � �      �   ,   x�3�ptwtq�2�p�s�t�q�2�ru�p����qqq �2      �   �   x����
�0����S����e��G�n��Z�D���[�ಋ�����b�,�e�}�9G*�O��D��x�x���a�4�k�5���;1��k�����lUo�
m��aڭ��Ts��^�j�k~��?���5L?Cs���^)�'��/<^�      �     x����N!�3�$�Kf���ѫb�iRw���|_L�xq7�n	7��g �����u�c���r�c������rֹ�+.%k�8ap�_��ސ8��aY8$
c;�²,�	,���㢰�vG�(�U�E�����?�,d�Pץ��o�����)�E����+}�_����-�A�]���$#1J�f{���/�.nBm�6�#w���*?b��b���[~=�5�w3N�0(pS�'d��)��Na�Iq^3&�} 	݋���T�      �   �   x�]�=�0���>LE(�c�Q	HQ$��C:��-C��q�~��$C���1�0���;�tZ�Wac�:�Xf+�l��߻6�x=��|=vq�z������'Sĉ$F���1��k���ڙM{�j]T�Ħ�vZ�G�y�l�3Z8���#�<��7D�����      �   �   x���1
�0���)�[J���f�fU�
%�)b[��x'O���JA����=Π:B�0���򦭌�NZ�HG�e,�e��6�Wի�]	�KQ�v�9�Ƕ�3��&S+&�I8&�� �`��6�U�����YN���z�����$�.��V�!ԣ���^I�r��y��	!o3�PZ      �   �   x���0k1L�A�������N,�T*���t6�sb;�s�:����@f7���`����޿j{5\��j�z��ݚ�-ׁ��B�������c|8�w@�wH�wP�wX���Y<蝾�S+����$E      �   ]   x�3�tO-J�+IUHIUpL����,.)JL�<�9�˘�1/1(��M֐!��_�e�l�s~^IbRfNfJb
�)�9(R��E�e�� b���� 	w2�      �      x�3�4�2�4������ ��      �   p  x����N�0�볧� am�u��+o�J�m%mф��l~�&��lYӞ�v�'H!�߬V�l�W��I�x��tX)�?C�Z?�E��?��zC�����,X�D��\��d��W��n�k��F�bk�u
�
�x��c[�	Fq�8��`5���9��9��.gm��th�(��D<�?��F��4��u�.�������*2��j�*�\?�W���u�wJ�֟ԅ6;m��l�'�0���{�V��}g�"�y��Zu$.��hz�K�8!_�w�1�q0�[}:���H�n��Q���is���!��f�f��l�hb�bj�%�^k{�	�3��F9M�;��{�2�6^�Em�6_m�$���<�ʚ��      �   *  x��Tێ�@}.��/0����D׹iFfVݝh&ٴM�M�s�뷺��w3��.�ΩS�e������~��I{�^F&L��x��Oص����E���V��B�ۏ ���04�����B�#���3�׻�U��~��q`SV��R���e-�^�ӳP.�}-�/�����4���i��hE�����f>�ށN�_>ǖC�5�U�
ќԺ!Gx��:�˼�<i�3�V��[h��4%6�k���o�٥\������/�ފ�f�61�{��ć��{{P��u�\۴��3�B��J	�N�@p$W�|�c�ִ*$��'�(��ݿ���fN�?Yf���'7�|J(��z�ʔ�g���rY����Rm�b��BM���]'��r98�)$������x~��q.m�#�k���e���C��Jdu*�Y=	�����2%���/�ƓZ�3�W�q�L���]���9������\)V��"|͢�?��k�C��>�Y��ۃ��v����f+�?��<�����]Nm�g%�;�e�%qw�     