
insert into t_emisor(emisor_nrodoc, emisor_razonsocial,emisor_usuariosunat, emisor_clavesunat, emisor_clave, estado) values('20600521226','CONTEXTOS ASOCIADOS S.A.','','','20600521226',1);
insert into t_emisor(emisor_nrodoc, emisor_razonsocial,emisor_usuariosunat, emisor_clavesunat, emisor_clave, estado) values('20600575661','Servicios Líder Cleaners SAC','','','20600575661',1);
																				  
insert into t_tipocpe(tipocpe_desc, tipocpe_cod, estado)values('Factura','01',1);
insert into t_tipocpe(tipocpe_desc, tipocpe_cod, estado)values('Boleta','03',1);
insert into t_tipocpe(tipocpe_desc, tipocpe_cod, estado)values('Nota de Débito','08',1);
insert into t_tipocpe(tipocpe_desc, tipocpe_cod, estado)values('Nota de Crédito','07',1);
insert into t_tipocpe(tipocpe_desc, tipocpe_cod, estado)values('Guía de Remision','09',1);
insert into t_tipocpe(tipocpe_desc, tipocpe_cod, estado)values('Retención','20',1);
insert into t_tipocpe(tipocpe_desc, tipocpe_cod, estado)values('Percepción','40',1);
insert into t_tipocpe(tipocpe_desc, tipocpe_cod, estado)values('Comunicación Baja','RA',1);
insert into t_tipocpe(tipocpe_desc, tipocpe_cod, estado)values('Resumen Reversión','RR',1);
insert into t_tipocpe(tipocpe_desc, tipocpe_cod, estado)values('Resumen Comprobante','RC',1);

insert into t_tipodoc(tipodoc_desc, tipodoc_cod, estado)values('DOC.TRIB.NO.DOM.SIN.RUC','0',1);
insert into t_tipodoc(tipodoc_desc, tipodoc_cod, estado)values('Documento Nacional de Identidad','1',1);
insert into t_tipodoc(tipodoc_desc, tipodoc_cod, estado)values('Carnet de extranjería','4',1);
insert into t_tipodoc(tipodoc_desc, tipodoc_cod, estado)values('Registro Unico de Contributentes','6',1);
insert into t_tipodoc(tipodoc_desc, tipodoc_cod, estado)values('Pasaporte','7',1);
insert into t_tipodoc(tipodoc_desc, tipodoc_cod, estado)values('DOC.IDENT.PAIS.RESIDENCIA-NO.D','B',1);
insert into t_tipodoc(tipodoc_desc, tipodoc_cod, estado)values('Tax Identification Number - TIN – Doc Trib PP.NN','C',1);
insert into t_tipodoc(tipodoc_desc, tipodoc_cod, estado)values('Identification Number - IN – Doc Trib PP. JJ','D',1);
insert into t_tipodoc(tipodoc_desc, tipodoc_cod, estado)values('TAM- Tarjeta Andina de Migración','E',1);
    
insert into t_estado(estado_desc, estado_cod, estado_tipo,estado_cond, estado) values('RECHAZADO', '99','','', 1);
insert into t_estado(estado_desc, estado_cod, estado_tipo,estado_cond, estado) values('PENDIENTE', '01','','', 1);
insert into t_estado(estado_desc, estado_cod, estado_tipo,estado_cond, estado) values('ACEPTADO', '0','','', 1);
insert into t_estado(estado_desc, estado_cod, estado_tipo,estado_cond, estado) values('ANULADO', '02','','', 1);
insert into t_estado(estado_desc, estado_cod, estado_tipo,estado_cond, estado) values('BAJA', '03','','', 1);
  
insert into t_usuario(usu_correo,usu_nombre,usu_cel,usu_pass) values('admin@pressto.pe','ADMIN','123456','ADMIN')

insert into t_tipodoc(tipodoc_id,tipodoc_desc, tipodoc_cod, estado) select * from t_tipodoc2;
select * from t_estado;
select * from t_estado2;

select * from t_tipocpe;
select * from t_estado;
select * from t_emisor;

select * from t_receptor;
insert into t_receptor(receptor_id,receptor_nrodoc, receptor_razonsocial)
select receptor_id,receptor_nrodoc, receptor_razonsocial, (select) from t_receptor2;
 