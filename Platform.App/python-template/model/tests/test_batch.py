

from utils.http import HttpClient, ExecutionResult
import json
from mock import patch
from model.batch import BatchPersistence



def head_of_process_memory():
    res = ExecutionResult(200)
    r = """
{
    "event": {
        "name": "calculate.tax.by.usina",
        "instance_id": null,
        "reference_date": null,
        "reproduction": {},
        "reprocess": {},
        "payload": {
            "dataFinalEvento": "2014-11-01T00:00:00.000Z",
            "dataInicialEvento": "2014-10-01T00:00:00.000Z",
            "idExecucaoCalculo": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
            "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
            "idUsina": "ALUXG"
        }
    },
    "processId": "591bb393-41a3-4634-8216-aa1281856fdb",
    "systemId": "eb60a12f-130d-4b8b-8b0d-a5f94d39cb0b",
    "instanceId": "ecb674bb-8958-4114-8383-7577758b055b",
    "eventOut": "calcularTaxasPorUsina.done",
    "commit": true,
    "map": {
        "_metadata": {
            "branch": "master",
            "type": "map"
        },
        "content": {
            "execucaocalculofechamento": {
                "model": "tb_exec_calc_fech",
                "fields": {
                    "id": {
                        "column": "id"
                    },
                    "dataInicio": {
                        "column": "data_inicio"
                    },
                    "dataFim": {
                        "column": "data_fim"
                    },
                    "idCenario": {
                        "column": "id_cenario"
                    },
                    "idTarefa": {
                        "column": "id_tarefa"
                    },
                    "protocolo": {
                        "column": "protocolo"
                    },
                    "idFechamento": {
                        "column": "id_fechamento"
                    }
                },
                "filters": {
                    "byId": "id = :idExecucaoCalculo"
                }
            },
            "fechamentomensal": {
                "model": "tb_fechamento_mensal",
                "fields": {
                    "id": {
                        "column": "id"
                    },
                    "mes": {
                        "column": "mes"
                    },
                    "ano": {
                        "column": "ano"
                    },
                    "dataCriacao": {
                        "column": "data_criacao"
                    }
                },
                "filters": {
                    "byId": "id = :idFechamento"
                }
            },
            "taxa": {
                "model": "tb_taxa",
                "fields": {
                    "idTipoTaxa": {
                        "column": "id_tipo_taxa"
                    },
                    "valorTaxa": {
                        "column": "valor"
                    },
                    "idFechamento": {
                        "column": "id_fechamento"
                    },
                    "idUsina": {
                        "column": "id_usina"
                    }
                },
                "filters": {
                    "byUsinaEFechamento": "id_usina = :idUsina and id_fechamento = :idFechamento"
                }
            },
            "usina": {
                "model": "tb_usina",
                "fields": {
                    "id": {
                        "column": "id",
                        "required": true
                    },
                    "idUsina": {
                        "column": "id_usina",
                        "required": true
                    },
                    "nome": {
                        "column": "nome",
                        "required": true
                    }
                },
                "filters": {
                    "byIdUsina": "id_usina = :idUsina"
                }
            },
            "unidadegeradora": {
                "model": "tb_unidade_geradora",
                "fields": {
                    "idUge": {
                        "column": "id_uge"
                    },
                    "potenciaDisponivel": {
                        "column": "pot_disp"
                    },
                    "dataInicioOperacao": {
                        "column": "data_inicio_operacao"
                    },
                    "idUsina": {
                        "column": "id_usina"
                    }
                },
                "filters": {
                    "byIdUsina": "id_usina = :idUsina"
                }
            },
            "eventomudancaestadooperativo": {
                "model": "tb_evt_estado_oper",
                "fields": {
                    "idEvento": {
                        "column": "id_evento"
                    },
                    "idUge": {
                        "column": "id_uge"
                    },
                    "idClassificacaoOrigem": {
                        "column": "id_class_origem"
                    },
                    "idEstadoOperativo": {
                        "column": "id_tp_estado_oper"
                    },
                    "idCondicaoOperativa": {
                        "column": "id_cond_oper"
                    },
                    "dataVerificada": {
                        "column": "data_verificada"
                    },
                    "potenciaDisponivel": {
                        "column": "pot_disp"
                    }
                },
                "filters": {
                    "byIntervaloDatas": "data_verificada >= :dataInicialEvento and data_verificada <= :dataFinalEvento"
                }
            },
            "parametrotaxa": {
                "model": "tb_parametro_taxa",
                "fields": {
                    "valorParametro": {
                        "column": "valor_parametro"
                    },
                    "idTipoParametro": {
                        "column": "id_tipo_parametro"
                    },
                    "idUge": {
                        "column": "id_uge"
                    },
                    "idFechamento": {
                        "column": "id_fechamento"
                    },
                    "idExecucaoCalculoFechamento": {
                        "column": "id_exec_calc_fech"
                    },
                    "mes": {
                        "column": "mes"
                    },
                    "ano": {
                        "column": "ano"
                    }
                },
                "filters": {
                    "byUsinaEFechamento": "id_fechamento = :idFechamento and id_exec_calc_fech = :idExecucaoCalculo"
                }
            }
        },
        "id": "a7554182-403d-4d4a-bdbe-75cb2ba1b38d",
        "name": "calculartaxasprocess",
        "processId": "591bb393-41a3-4634-8216-aa1281856fdb",
        "systemId": "eb60a12f-130d-4b8b-8b0d-a5f94d39cb0b"
    },
    "dataset": {
        "execucaocalculofechamento": {
            "collection": {
                "prevSource": {}
            }
        },
        "fechamentomensal": {
            "collection": {
                "prevSource": {}
            }
        },
        "taxa": {
            "collection": {
                "prevSource": {}
            }
        },
        "usina": {
            "collection": {
                "prevSource": {}
            }
        },
        "unidadegeradora": {
            "collection": {
                "prevSource": {}
            }
        },
        "eventomudancaestadooperativo": {
            "collection": {
                "prevSource": {}
            }
        },
        "parametrotaxa": {
            "collection": {
                "prevSource": {}
            }
        },
        "entities": {
            "execucaocalculofechamento": [],
            "fechamentomensal": [
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "fechamentomensal"
                    },
                    "ano": 2014,
                    "dataCriacao": "2018-03-13T00:00:00.000Z",
                    "id": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "mes": 10
                }
            ],
            "taxa": [
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "taxa",
                        "changeTrack": "update"
                    },
                    "id": "fb6c98ab-ea90-f534-4ecf-53a2a7849cd8",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idTipoTaxa": "TEIPmes",
                    "idUsina": "ALUXG",
                    "valorTaxa": 0.010752688172043012
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "taxa",
                        "changeTrack": "update"
                    },
                    "id": "8a71ab13-8df7-5b6e-76ea-fe3b9c5eb95b",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idTipoTaxa": "TEIFAmes",
                    "idUsina": "ALUXG",
                    "valorTaxa": 0.17204301075268819
                }
            ],
            "usina": [
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "usina"
                    },
                    "id": "db187a6a-6fcd-4762-8206-d4ee8aa91b97",
                    "idUsina": "ALUXG",
                    "nome": "ALUXG"
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "usina"
                    },
                    "id": "945ec8f4-74d5-4609-a6f8-b31c441ac746",
                    "idUsina": "ALUXG",
                    "nome": "ALUXG"
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "usina"
                    },
                    "id": "c1702c23-f5fd-4bdc-8c33-ef82432b22d3",
                    "idUsina": "ALUXG",
                    "nome": "ALUXG"
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "usina"
                    },
                    "id": "df6c22bc-6282-4ad2-bbdb-5557b2872754",
                    "idUsina": "ALUXG",
                    "nome": "ALUXG"
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "usina"
                    },
                    "id": "d58629ed-d0a3-4f94-86bf-86fa1caa3b45",
                    "idUsina": "ALUXG",
                    "nome": "ALUXG"
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "usina"
                    },
                    "id": "e89b6b4e-396f-47e7-b71a-c9e0069f38a2",
                    "idUsina": "ALUXG",
                    "nome": "ALUXG"
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "usina"
                    },
                    "id": "222fa8fd-93d2-43b4-8287-a5a960f5af15",
                    "idUsina": "ALUXG",
                    "nome": "ALUXG"
                }
            ],
            "unidadegeradora": [
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1997-08-22T00:00:00.000Z",
                    "id": "8dce7127-09ae-40fe-adf0-ee6587eddcc7",
                    "idUge": "ALUXG-0UG1",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-12-20T00:00:00.000Z",
                    "id": "f3486a03-2085-4381-99f5-8b02b73db823",
                    "idUge": "ALUXG-0UG2",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-07-31T00:00:00.000Z",
                    "id": "71734e83-2a2c-4569-8ab6-be4500a6b4df",
                    "idUge": "ALUXG-0UG3",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-10-26T00:00:00.000Z",
                    "id": "c6e52d45-5f0a-4842-bb9c-2ee1494e7fac",
                    "idUge": "ALUXG-0UG4",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-01-31T00:00:00.000Z",
                    "id": "ab27344b-5a45-435e-903c-3ab8210a599a",
                    "idUge": "ALUXG-0UG5",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1994-04-30T00:00:00.000Z",
                    "id": "6548d69a-4947-426f-bc3c-1fda59c787f7",
                    "idUge": "ALUXG-0UG6",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1997-08-22T00:00:00.000Z",
                    "id": "cf4146ac-f310-4d6b-84ea-622f8796f8d4",
                    "idUge": "ALUXG-0UG1",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-12-20T00:00:00.000Z",
                    "id": "c721d717-0146-4e3b-b3e6-f23459940103",
                    "idUge": "ALUXG-0UG2",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-07-31T00:00:00.000Z",
                    "id": "86120131-be62-44eb-b687-824e311438cb",
                    "idUge": "ALUXG-0UG3",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-10-26T00:00:00.000Z",
                    "id": "f7fb77fe-7148-48d3-aaf0-036501af0470",
                    "idUge": "ALUXG-0UG4",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-01-31T00:00:00.000Z",
                    "id": "65a174a2-4589-42bb-9531-a69b1dbcd590",
                    "idUge": "ALUXG-0UG5",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1994-04-30T00:00:00.000Z",
                    "id": "f98d828c-a0c1-4104-968a-ae30aca3390c",
                    "idUge": "ALUXG-0UG6",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1997-08-22T00:00:00.000Z",
                    "id": "4a16b0e9-8fbd-4355-8b20-51271ebf0d63",
                    "idUge": "ALUXG-0UG1",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-12-20T00:00:00.000Z",
                    "id": "cec4b128-79e9-4d45-b171-a7b920d89264",
                    "idUge": "ALUXG-0UG2",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-07-31T00:00:00.000Z",
                    "id": "4cae4dbc-5272-4229-8334-dc67cc2653ab",
                    "idUge": "ALUXG-0UG3",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-10-26T00:00:00.000Z",
                    "id": "c5004730-adaf-4105-9cd2-d76feeb591c6",
                    "idUge": "ALUXG-0UG4",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-01-31T00:00:00.000Z",
                    "id": "bb9443c8-1990-4965-ab12-a75e815a5e20",
                    "idUge": "ALUXG-0UG5",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1994-04-30T00:00:00.000Z",
                    "id": "92b844cc-c0e1-459f-a990-3c120d02abcd",
                    "idUge": "ALUXG-0UG6",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1997-08-22T00:00:00.000Z",
                    "id": "cb377073-d50c-452e-adea-2fd97b2ec592",
                    "idUge": "ALUXG-0UG1",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-12-20T00:00:00.000Z",
                    "id": "f14e1962-4047-483a-8c16-a5b6cb98596e",
                    "idUge": "ALUXG-0UG2",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-07-31T00:00:00.000Z",
                    "id": "999cbcd3-d117-49ae-b4af-2fbc409e6458",
                    "idUge": "ALUXG-0UG3",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-10-26T00:00:00.000Z",
                    "id": "30997afb-c741-401d-acc3-091762a610ff",
                    "idUge": "ALUXG-0UG4",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-01-31T00:00:00.000Z",
                    "id": "aa3658d8-e59d-4b4a-8c2d-9026ffedbfe5",
                    "idUge": "ALUXG-0UG5",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1994-04-30T00:00:00.000Z",
                    "id": "d9667d61-38ad-483e-a3cb-f29dab886927",
                    "idUge": "ALUXG-0UG6",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1997-08-22T00:00:00.000Z",
                    "id": "e32a7761-c407-42dd-aa08-1dd62d8017b0",
                    "idUge": "ALUXG-0UG1",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-12-20T00:00:00.000Z",
                    "id": "ac5aa955-69e8-4595-93a2-36a2f9438273",
                    "idUge": "ALUXG-0UG2",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-07-31T00:00:00.000Z",
                    "id": "7aba0ccf-8482-4c3f-a14c-a2eda520ea48",
                    "idUge": "ALUXG-0UG3",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-10-26T00:00:00.000Z",
                    "id": "ebc8c985-3d81-41f6-b86f-ae6ff7e59b3c",
                    "idUge": "ALUXG-0UG4",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-01-31T00:00:00.000Z",
                    "id": "6007842b-d6a5-4c46-b95d-371c3eb7282c",
                    "idUge": "ALUXG-0UG5",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1994-04-30T00:00:00.000Z",
                    "id": "0ed30fe7-ad10-4e10-9253-cce495020f1a",
                    "idUge": "ALUXG-0UG6",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1997-08-22T00:00:00.000Z",
                    "id": "0e8a3075-575b-4da3-9f6c-c31ad356b448",
                    "idUge": "ALUXG-0UG1",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-12-20T00:00:00.000Z",
                    "id": "497f9fad-fb8e-4ee1-a981-afd1943796e8",
                    "idUge": "ALUXG-0UG2",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-07-31T00:00:00.000Z",
                    "id": "7a0ff3a7-516b-4f8a-902b-cafc903a7538",
                    "idUge": "ALUXG-0UG3",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-10-26T00:00:00.000Z",
                    "id": "02505832-52ba-4e3d-96cf-e4d8c61f8e9e",
                    "idUge": "ALUXG-0UG4",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-01-31T00:00:00.000Z",
                    "id": "71ecef6a-ea7d-4ad3-a260-f61b6e41aa79",
                    "idUge": "ALUXG-0UG5",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1994-04-30T00:00:00.000Z",
                    "id": "3c4998b7-ee16-451d-a7fe-d81a92d19d08",
                    "idUge": "ALUXG-0UG6",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1997-08-22T00:00:00.000Z",
                    "id": "3912780e-ea50-4141-b784-aee1166f535c",
                    "idUge": "ALUXG-0UG1",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-12-20T00:00:00.000Z",
                    "id": "fab96911-e325-4331-9d60-96e80adecf5d",
                    "idUge": "ALUXG-0UG2",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1996-07-31T00:00:00.000Z",
                    "id": "531e7b54-25a4-4380-bd5b-6ab41a0b9776",
                    "idUge": "ALUXG-0UG3",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-10-26T00:00:00.000Z",
                    "id": "21873331-8770-4f48-b308-d42e9688f09d",
                    "idUge": "ALUXG-0UG4",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1995-01-31T00:00:00.000Z",
                    "id": "2b995057-b574-4717-8b9f-dc1710d53dd8",
                    "idUge": "ALUXG-0UG5",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "unidadegeradora"
                    },
                    "dataInicioOperacao": "1994-04-30T00:00:00.000Z",
                    "id": "cbdc01af-51ed-4cff-8ea1-0d7f1fd4397a",
                    "idUge": "ALUXG-0UG6",
                    "idUsina": "ALUXG",
                    "potenciaDisponivel": 527
                }
            ],
            "eventomudancaestadooperativo": [
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "287b7e22-1a6a-4673-9b50-a13aa9fa20d1",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2392231",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1412121600,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-13T00:00:00.000Z",
                    "id": "732d563c-d983-404f-a4ee-e726cf48ae2a",
                    "idClassificacaoOrigem": "GTR",
                    "idCondicaoOperativa": "",
                    "idEstadoOperativo": "DEM",
                    "idEvento": "2398574",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 0,
                    "dataVerificadaEmSegundos": 1413158400,
                    "tiposParametrosComputados": [
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF"
                    ],
                    "duracaoEmSegundos": 0
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-14T00:00:00.000Z",
                    "id": "c5e1160e-03d3-4e72-8cd5-2cc492f46129",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "TST",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2399096",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413244800,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-17T00:00:00.000Z",
                    "id": "6ac89869-aea1-454e-9bed-d9f4041fa90f",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "TST",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401532",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413504000,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-17T00:00:00.000Z",
                    "id": "f2efc70a-15a2-4498-bd08-ce3ab50a1fce",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401533",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413504000,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-18T00:00:00.000Z",
                    "id": "69c5f8de-8add-420d-a083-0c68ebcb756e",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2401534",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413590400,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-19T00:00:00.000Z",
                    "id": "084ae966-c166-4858-81c4-be01e04d7048",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "TST",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401535",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413676800,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-19T00:00:00.000Z",
                    "id": "3dba7cbc-3907-4a12-873b-678a086dfa70",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOT",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401536",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413676800,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-20T00:00:00.000Z",
                    "id": "f011addd-435e-45f9-8493-bdafcc2a01a1",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401537",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413763200,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "ef255d74-40b5-43f8-afa2-4e7387aed262",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2407662",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414800000
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "3e810221-ed2d-4e92-8178-6b01317bd165",
                    "idClassificacaoOrigem": "GUM",
                    "idCondicaoOperativa": "",
                    "idEstadoOperativo": "DAU",
                    "idEvento": "2392232",
                    "idUge": "ALUXG-0UG2",
                    "potenciaDisponivel": 0,
                    "dataVerificadaEmSegundos": 1412121600,
                    "tiposParametrosComputados": [
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF"
                    ],
                    "duracaoEmSegundos": 0
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "8ca549b9-f3ca-4445-afd8-771663e2969b",
                    "idClassificacaoOrigem": "GUM",
                    "idCondicaoOperativa": "",
                    "idEstadoOperativo": "DAU",
                    "idEvento": "2407663",
                    "idUge": "ALUXG-0UG2",
                    "potenciaDisponivel": 0,
                    "dataVerificadaEmSegundos": 1414800000
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "613d0865-ba3c-42cc-a6fd-bf626ea5f777",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2392233",
                    "idUge": "ALUXG-0UG3",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1412121600,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "2e302639-c16f-4b10-a9e5-fb1578a59fc6",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2407664",
                    "idUge": "ALUXG-0UG3",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414800000
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "d908fb94-3565-4db8-8781-673de8275849",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2392234",
                    "idUge": "ALUXG-0UG4",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1412121600,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-19T00:00:00.000Z",
                    "id": "2e53ebd1-3c3b-4db8-bffd-2f8fb27f3386",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2401538",
                    "idUge": "ALUXG-0UG4",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413676800,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "fc995f65-7ed5-4840-8588-7127fc8e3d3f",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2407665",
                    "idUge": "ALUXG-0UG4",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414800000
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "beb18dbb-4f74-4b15-aff3-1336f00dff2f",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2392235",
                    "idUge": "ALUXG-0UG5",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1412121600,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-13T00:00:00.000Z",
                    "id": "a2b1ad30-bcd5-45e0-9b85-a86fa5957547",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2398575",
                    "idUge": "ALUXG-0UG5",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413158400,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "81065513-c649-4fa9-b08f-646e7ae01d35",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2407666",
                    "idUge": "ALUXG-0UG5",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414800000
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "eca59229-e99a-420c-8016-8847efb398e2",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2392236",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1412121600,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-13T00:00:00.000Z",
                    "id": "a583c13a-03c3-41b0-8ab9-da8987158734",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2398576",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413158400,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-14T00:00:00.000Z",
                    "id": "9323a6cc-c4c4-4648-8cf1-609c105707e7",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2399097",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413244800,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-17T00:00:00.000Z",
                    "id": "e68dea1b-2818-4aaa-ad15-06162c3ec111",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401539",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413504000,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-18T00:00:00.000Z",
                    "id": "1f47c4b1-bec1-4674-8512-1f535315bf9c",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2401540",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413590400,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-22T00:00:00.000Z",
                    "id": "112810a0-e393-4b15-81ef-e36149c52e0c",
                    "idClassificacaoOrigem": "GTR",
                    "idCondicaoOperativa": "",
                    "idEstadoOperativo": "DPR",
                    "idEvento": "2403480",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 0,
                    "dataVerificadaEmSegundos": 1413936000,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HDP",
                        "HDP",
                        "HDP",
                        "HDP",
                        "HDP",
                        "HDP",
                        "HDP"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-24T00:00:00.000Z",
                    "id": "1861919d-3bbc-40c9-bf52-4ea9be0c7ceb",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "TST",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2405596",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414108800,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-30T00:00:00.000Z",
                    "id": "5686cbd1-2ab2-4e96-802e-2054640b92a0",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2407222",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414627200,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-30T00:00:00.000Z",
                    "id": "581d3173-43a9-4da8-b0a0-41e72db28fda",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2407223",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414627200,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "6227c241-814a-46ca-9aab-880ca945a8af",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2407667",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414800000
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "2c48ba53-4361-4fe2-8154-c8de2a740f2d",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2392231",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1412121600,
                    "duracaoEmSegundos": 1036800,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-13T00:00:00.000Z",
                    "id": "0602f050-30bc-48d0-8da9-a3360bce2f59",
                    "idClassificacaoOrigem": "GTR",
                    "idCondicaoOperativa": "",
                    "idEstadoOperativo": "DEM",
                    "idEvento": "2398574",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 0,
                    "dataVerificadaEmSegundos": 1413158400,
                    "tiposParametrosComputados": [
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF"
                    ],
                    "duracaoEmSegundos": 86400
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-14T00:00:00.000Z",
                    "id": "1e3e1d45-9c39-48f5-acae-8f1e81e5f170",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "TST",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2399096",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413244800,
                    "duracaoEmSegundos": 259200,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-17T00:00:00.000Z",
                    "id": "5ea80a64-ae42-4306-9e8e-fd1157e1d001",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "TST",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401532",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413504000,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-17T00:00:00.000Z",
                    "id": "9b96fb20-59c3-49c2-a821-3b7778b021fa",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401533",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413504000,
                    "duracaoEmSegundos": 86400,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-18T00:00:00.000Z",
                    "id": "b854d695-e3e0-4ac2-8c30-e3b4efcdc097",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2401534",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413590400,
                    "duracaoEmSegundos": 86400,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-19T00:00:00.000Z",
                    "id": "58dc77af-71b7-4f4f-811c-56934a81135d",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "TST",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401535",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413676800,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-19T00:00:00.000Z",
                    "id": "cc1a4552-9ba5-4693-8fce-4c1f47bcaff4",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOT",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401536",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413676800,
                    "duracaoEmSegundos": 86400,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-20T00:00:00.000Z",
                    "id": "780154a4-0877-4387-a0dc-c2d7760aa3b3",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401537",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413763200,
                    "duracaoEmSegundos": 1036800,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "b397fcc4-73ac-4f6a-815c-ec3f6ec573fa",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2407662",
                    "idUge": "ALUXG-0UG1",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414800000
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "50a05726-6512-45ab-ac6b-e01f8f341686",
                    "idClassificacaoOrigem": "GUM",
                    "idCondicaoOperativa": "",
                    "idEstadoOperativo": "DAU",
                    "idEvento": "2392232",
                    "idUge": "ALUXG-0UG2",
                    "potenciaDisponivel": 0,
                    "dataVerificadaEmSegundos": 1412121600,
                    "tiposParametrosComputados": [
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF",
                        "HDF"
                    ],
                    "duracaoEmSegundos": 2678400
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "a1b5b90f-5ea5-4302-a491-96d033434b34",
                    "idClassificacaoOrigem": "GUM",
                    "idCondicaoOperativa": "",
                    "idEstadoOperativo": "DAU",
                    "idEvento": "2407663",
                    "idUge": "ALUXG-0UG2",
                    "potenciaDisponivel": 0,
                    "dataVerificadaEmSegundos": 1414800000
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "66a56be0-32e0-447d-a80d-9c123fbbd2a0",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2392233",
                    "idUge": "ALUXG-0UG3",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1412121600,
                    "duracaoEmSegundos": 2678400,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "b6095b88-e893-499e-8ca9-49d5d8dd5245",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2407664",
                    "idUge": "ALUXG-0UG3",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414800000
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "9dbf26bd-0673-4e00-87ee-198f24f9f408",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2392234",
                    "idUge": "ALUXG-0UG4",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1412121600,
                    "duracaoEmSegundos": 1555200,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-19T00:00:00.000Z",
                    "id": "9c3384e5-6d29-4ca2-b946-04dd13c2d098",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2401538",
                    "idUge": "ALUXG-0UG4",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413676800,
                    "duracaoEmSegundos": 1123200,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "68e24ca6-f0b7-4ed2-ab8d-660148e353ba",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2407665",
                    "idUge": "ALUXG-0UG4",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414800000
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "722756bf-1fa7-4284-be11-cfd78e291795",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2392235",
                    "idUge": "ALUXG-0UG5",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1412121600,
                    "duracaoEmSegundos": 1036800,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-13T00:00:00.000Z",
                    "id": "c007a8e1-5c01-4438-8754-be8dc7c52b5d",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2398575",
                    "idUge": "ALUXG-0UG5",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413158400,
                    "duracaoEmSegundos": 1641600,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "487957bf-3c09-4e4c-b7b1-46d3a35f4ebf",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2407666",
                    "idUge": "ALUXG-0UG5",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414800000
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-01T00:00:00.000Z",
                    "id": "30af3eae-579f-4fdd-a962-69d0b21c0ddb",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2392236",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1412121600,
                    "duracaoEmSegundos": 1036800,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-13T00:00:00.000Z",
                    "id": "6e01ccfd-f9fe-4159-b51c-50692d5eaebe",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2398576",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413158400,
                    "duracaoEmSegundos": 86400,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-14T00:00:00.000Z",
                    "id": "95b2d644-240c-49e4-8dc2-63e144216f96",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2399097",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413244800,
                    "duracaoEmSegundos": 259200,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-17T00:00:00.000Z",
                    "id": "01a48598-7acb-4b20-bb24-5fe4f4869232",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2401539",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413504000,
                    "duracaoEmSegundos": 86400,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-18T00:00:00.000Z",
                    "id": "d6fbf23a-9093-4f49-a104-f00a7c99369c",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2401540",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1413590400,
                    "duracaoEmSegundos": 345600,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-22T00:00:00.000Z",
                    "id": "7a9990b6-8dff-4a0b-9a57-88c59d14f212",
                    "idClassificacaoOrigem": "GTR",
                    "idCondicaoOperativa": "",
                    "idEstadoOperativo": "DPR",
                    "idEvento": "2403480",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 0,
                    "dataVerificadaEmSegundos": 1413936000,
                    "duracaoEmSegundos": 172800,
                    "tiposParametrosComputados": [
                        "HDP",
                        "HDP",
                        "HDP",
                        "HDP",
                        "HDP",
                        "HDP",
                        "HDP"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-24T00:00:00.000Z",
                    "id": "c6e018df-b01c-4492-988a-9ca199952eda",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "TST",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2405596",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414108800,
                    "duracaoEmSegundos": 518400,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-30T00:00:00.000Z",
                    "id": "48e4eba5-c288-40e3-9918-6051514fc44a",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "LIG",
                    "idEvento": "2407222",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414627200,
                    "duracaoEmSegundos": 0,
                    "tiposParametrosComputados": [
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS",
                        "HS"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-10-30T00:00:00.000Z",
                    "id": "44d4b7c8-cd42-4ea7-b718-87561e3e9ad3",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2407223",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414627200,
                    "duracaoEmSegundos": 172800,
                    "tiposParametrosComputados": [
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD",
                        "HRD"
                    ]
                },
                {
                    "_metadata": {
                        "branch": "master",
                        "type": "eventomudancaestadooperativo"
                    },
                    "dataVerificada": "2014-11-01T00:00:00.000Z",
                    "id": "777a580f-5627-4289-92ba-5bf9b5a89e23",
                    "idClassificacaoOrigem": "",
                    "idCondicaoOperativa": "NOR",
                    "idEstadoOperativo": "DCO",
                    "idEvento": "2407667",
                    "idUge": "ALUXG-0UG6",
                    "potenciaDisponivel": 527,
                    "dataVerificadaEmSegundos": 1414800000
                }
            ],
            "parametrotaxa": [
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "43661826-f8f3-82fe-6496-0a1314f1c189",
                    "valorParametro": 24,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "5ee93ac0-d328-0423-187b-4fb2adde9b39",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "b25f6735-986f-65ef-3a1c-1391983d8be2",
                    "valorParametro": 624,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "6714e053-5519-5731-f752-505dde079bba",
                    "valorParametro": 96,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "e7705545-d348-fb80-c7ed-971c113f85b0",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "b715b40e-a1a5-9828-a31e-038bc8266c10",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "32c4b574-8664-93b5-d0b5-0d15f5fd587c",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "405923c2-08e7-36f7-87a0-5684a9182be1",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ebcf8d6f-ea43-fccf-cb9a-554248afc672",
                    "valorParametro": 744,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ef1922f2-deaa-c817-45a4-c36ee9e93083",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ac74c01d-2985-1370-426a-fb957fecd22c",
                    "valorParametro": 0,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f6b14657-83ac-b56e-4428-e60e47fa0e41",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "10800d78-fb2b-1a75-71c6-06c1459644ed",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "54b7eb01-76f4-f27f-469d-cbf2b16ec245",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "bb8ce819-b820-e83d-dda2-7c57f946beff",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7f79dd02-faed-3f37-e869-f994975edb1b",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "149c744a-1667-f4f6-6959-bb800bd98206",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "4522f3e9-c216-89a9-87a3-c162fe611bb1",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7e97d197-d881-76b3-aecf-2a37f9393e9e",
                    "valorParametro": 744,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c07a8db0-9f04-f32d-ad81-dfa2a7c48fbf",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "05865143-fe15-3148-eb00-e1dc12c295a4",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c372991c-b284-e42f-ee28-6cd408517a35",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "92cd2730-9dbe-6f26-6f12-e2d841cd55ab",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "cff6bb92-220d-bbaa-f198-ab2d2c510893",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "aa18fba9-7e7f-278e-2c06-b40d4719e863",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "764c4c24-c793-35ac-7f5a-7ba34643bcfa",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "da7925e5-9264-3e26-8b26-76d1ec435b56",
                    "valorParametro": 432,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "53257d2e-d6ac-54f5-5bb9-04226606bfeb",
                    "valorParametro": 312,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "db7a6d73-0199-44a5-d4d5-60177c41aaa5",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "093168a4-a80e-0912-df79-7bc1cb4ce229",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "8f01e3cb-f744-7f48-3e40-5eeaf11f6bbf",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9c0fdd25-5a58-3a68-738e-a274761ca9ec",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "10c7c5c9-1238-5f70-04f5-ddc423974f8d",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "67f9b8a7-8d16-5f23-29b8-527980ef25d4",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "345f4cb5-c4bd-60f4-fa30-91f6e1893352",
                    "valorParametro": 456,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9a219b18-a4f9-c7c1-7920-6b2664080df4",
                    "valorParametro": 288,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c239dae9-b969-20c1-262f-2d71accc5599",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "21e61b61-60b7-0b5d-def8-30fa03cafae4",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "eef1d3f6-03c9-5ae9-4c3c-d1f0bc11d385",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d15e4b88-aa61-b01d-04f2-d78d0abb3fc8",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f148c9d7-c20f-7f46-491e-e50d4d26d9ce",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "90c26cd5-10ad-9806-1989-ed1fdb9f3d08",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "3f4aae7b-3f20-b2ee-88f5-a4d0c7939b71",
                    "valorParametro": 48,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "15d52c33-9e56-8f89-c0e4-f8b65706c7da",
                    "valorParametro": 648,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "06381bdd-fd5c-8596-cd11-acfb830c1d92",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "33a292c6-8f05-d820-4c63-d76f1dc71f60",
                    "valorParametro": 48,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ae3f6a40-a5f1-f931-567d-425a68377816",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f554ea50-dce1-d30d-0faf-c387ff0b77aa",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "bb0a8d3b-11b6-5b1f-ca6f-cee8ebc9319f",
                    "valorParametro": 24,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "dcd2b816-c3c5-0107-0a05-7c7cb27c78bc",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "e8bda0d4-52ee-118d-46bc-14da2093fb0b",
                    "valorParametro": 624,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "0fa89909-3a39-7fd4-b12f-2d117c3c303a",
                    "valorParametro": 96,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "417a9e8c-e0ea-d321-f67c-9f0a3a93e2a2",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a3a7f48f-cf8c-d840-fb72-a93b5af131e1",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "5749702f-c9aa-122e-68f1-be592aaf693c",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "89225c50-f750-c9ca-d818-5a2341fd5458",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1150260d-4f23-92fb-0dfd-c733e8ccaed6",
                    "valorParametro": 744,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "8fbc991a-a753-f4ed-dd3f-78ba1fda7aeb",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1a539b08-d459-2f37-5f62-c381badfcc0f",
                    "valorParametro": 0,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a180070f-3b4b-ef07-31ad-b4b102b9a1f0",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "56b3ba79-d305-fee9-ce6a-2902059fff87",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "b506f01a-54a9-5065-f430-d934043353d2",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f702ac3d-ae49-12c5-e29b-a3a522def21a",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "233783cb-bc46-9df4-7d1a-fcac6854883d",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "60dd1dbf-003a-e1cc-4643-ae8a6b44cf01",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "98f75917-c8fe-214a-6538-93b2fbe0f605",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "13b845bc-bb15-3c4c-e84f-15ecef7fc25d",
                    "valorParametro": 744,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "aba7a982-f00e-b870-dbf9-698a9b9b63bd",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "0f193c2d-e987-36c1-8dd9-97ee7f0aed5c",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "3d5afd8d-05d4-2c94-c165-076c33989cfd",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "47294f69-c89e-fdb0-35a7-79ccafc86d46",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c1c09f23-af9c-2f28-fc56-e13a1f3e0fd5",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "3c44ed3c-7aec-8038-55e5-6d6312dd4245",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "fd520c9f-4ea3-1aa7-214b-34ea2a6ec0dc",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d2a26147-9218-371c-4d33-8363ca84fc18",
                    "valorParametro": 432,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "34dfa77d-4445-f65b-1e10-f320b488a0c9",
                    "valorParametro": 312,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7be926de-aff3-3740-f91a-530f2fdf8442",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "22b2ce6d-5b0c-5c59-e0e0-984794ebfea2",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "75f1ca0f-6656-b313-e81b-fe184df74161",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "643e5d43-b0ad-db83-3089-4ac75590394a",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c473dd05-f9cf-0768-ca50-54d8bfa4eea1",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a02c8aa2-7b1a-713e-c678-113f0a385f0e",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "99455456-ac43-6745-3568-0fe12ebf33e1",
                    "valorParametro": 456,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "2d396348-99b7-70b2-8d0e-bc120c2cee2a",
                    "valorParametro": 288,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "25d9ba54-3dbd-a034-d517-102cbb252122",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "911e061b-7fe3-a75c-5f2d-af60e0ab3d40",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "6eea059e-c5f8-30da-5458-3a1a90a3c5d9",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "5b4e8c2c-a41c-5002-fb25-e8d435c5588b",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "90b2be8f-e702-c2ec-4dce-1c0ac8c1dd35",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "2df4ecbd-e56d-a197-2e30-ae3cd809478a",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "5a2fe322-e4a7-78a3-4a32-530504382fcc",
                    "valorParametro": 48,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "4cc10f0d-d998-c9e8-e7b9-1b81549b1189",
                    "valorParametro": 648,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "0d45992b-51bf-ec3d-450f-98351952b766",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c2847cab-ee66-778c-57fb-dc10cc9f4b3e",
                    "valorParametro": 48,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "15915299-92c7-953d-9f0f-0a19e9eea795",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "bc6fa9aa-00ed-3848-2224-43b185f0a255",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f9c14150-8f1a-54dc-caf2-9e4c7c7fe1b5",
                    "valorParametro": 24,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "abb32cb0-758b-044b-6214-5aa0247bd60a",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "975db5d5-f29a-8200-56f6-b3fadef4e22e",
                    "valorParametro": 624,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1cc1edc3-7e87-ddbd-2192-d77204126a9f",
                    "valorParametro": 96,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a217a822-dfde-a9a4-3944-b79d5b04afe5",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "62944792-1020-8e8f-33e2-b7c788096408",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9d6bcbdd-ec1c-f6c5-1ef1-813825a260bc",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "e7087735-84c2-7850-ec3c-aa68a19fb74c",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ef2bf033-3947-1ccf-f2c2-bf0ea7512291",
                    "valorParametro": 744,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ac656529-6a2d-ec78-fd45-b11b3c7d764f",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "44bccb58-9272-85cd-23f6-98ef679079ed",
                    "valorParametro": 0,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "932637d2-1fe2-4861-06dd-10d06c8cda4b",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ddfaa2e3-5b1c-18cd-fc93-20c1d689d311",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "be0056f3-9ccf-98c1-3062-9362821f6af1",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "8707faeb-fa9d-67de-2207-42fae20e7f64",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "4626183e-4d5c-652a-43b1-96fc1f6b1e98",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "91821cb3-f8af-31c5-984b-88a20308c122",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "52cfbb99-31de-36d1-bc3c-bda0e5c4610c",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f6c15996-f41f-50a1-61cd-844246dcb204",
                    "valorParametro": 744,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "96395592-03e5-abed-fd44-0b1e59b1521d",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "b249d352-a9e4-399f-1757-ba15bab9b853",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d4539469-363e-f90d-88e5-1217520e687e",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "2738fd42-b06c-ef15-bb58-859f856d9d68",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c9ad249f-beeb-bc03-cf4c-bc95a773b97f",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "dd78a350-7a82-92ae-aab3-387073cc7e5a",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1f7ccdc8-e069-305b-3788-7115d052ff1d",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ff9c4010-680a-96aa-239a-eae4f30d5b40",
                    "valorParametro": 432,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a4a3708a-0989-11ca-74a8-62ffae0cbb00",
                    "valorParametro": 312,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "b9147772-523b-09a1-374f-a83af0368efb",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "76b5a1f6-5128-789e-82ae-eafa52a3db3f",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "fe03a1e9-a099-76fd-cf02-37db219df1b7",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "fec0fa63-61cc-d891-3e29-9b5c933fa331",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "260c7720-038b-cef2-947f-dfa1123f4530",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "20c475c1-d85c-c056-be51-605653dcdc40",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "4c118e3f-3d76-4bbb-e8fa-158b0f41f377",
                    "valorParametro": 456,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "16ea486c-f503-4bd6-9e8a-017dc1bd77b0",
                    "valorParametro": 288,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "20e54e97-ff6d-98a2-88e3-38f4051bbbfd",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d21c6528-faa7-9bcc-f9e9-2c1d37eefe1a",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "4a81e9af-6890-e77e-2d8e-752515440ffa",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "aa3acdba-9404-09cd-d78f-04748c6867b1",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c659e8d2-1e10-30c5-6c7f-702a2c466a91",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "536c5dd4-5ff4-3d39-ca18-6787733d74fc",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "2e298db6-08c5-6ea3-63fe-62e54b5a7282",
                    "valorParametro": 48,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "fa5dd0e1-dc1c-11f4-724c-f19ab74a398b",
                    "valorParametro": 648,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7520244e-c1ca-a85d-3fb5-36aaeff38a08",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "92da7f76-4b65-d2ea-4dc6-efc4d646805f",
                    "valorParametro": 48,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "070b61c5-78af-ed30-0828-50c94f5a5c3a",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "23d95a35-428c-a7ac-fb11-3164dda6484a",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c5f94fff-9bc0-d589-c7d6-11b850c0e94b",
                    "valorParametro": 24,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "24dcb760-4ad3-e63e-7750-1d24b2e54451",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7bac686f-e72f-6935-4ef8-57f54ca484e1",
                    "valorParametro": 624,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "6df7a2d1-2b88-3398-42d8-06591a7af925",
                    "valorParametro": 96,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "99cf8b85-c3d7-7a39-a82c-1676e21ab23e",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "3303da77-5591-5726-addc-39f3a7d6503d",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c3712952-61e2-2225-f8e4-9b1056c36a61",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "072ca9a0-0664-04cb-027c-a2629eab297a",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d16e4aef-6337-3210-2158-5d9e24693beb",
                    "valorParametro": 744,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f02d211f-d64a-6798-f44c-5cbda67bdeeb",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "967367c8-4440-70c7-9e59-8b24eee08261",
                    "valorParametro": 0,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "0e9e003b-3072-c83c-4bd5-7c85710bd989",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7ada8a07-16f3-64f1-93ff-88e8381e271a",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ece66934-905f-6a70-7e3a-9c7b3752ae60",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "956cf966-b8b3-945c-f2cb-97236774269f",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "243d4cca-e1ac-0381-5dc3-e406491f6a81",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "e21e721e-83cd-fcd6-e3d0-75cfd5c0b21f",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "92f06102-a4b9-be92-812e-0183829dbe32",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "5b2eb13a-026f-fce1-bd53-f65a11d3943a",
                    "valorParametro": 744,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1829cf9c-d48f-d1c0-bd31-1f1f6cece5b6",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d6c288b4-0e90-3e54-188b-3d574e3deb0e",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "6f69fb6e-e69d-c82b-2c4a-8809e7d98417",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "11b5a1af-8c70-ec75-995e-bf704d5bb74e",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "23c9325d-6c86-c9a4-1eab-586e1f561971",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ff7662df-d6b5-133c-2f55-93a4c13e5d15",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1ed2bff2-44d0-3132-59de-56725cf7702c",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ea8abbc0-a1cd-e88e-e34d-be610ef6cf6f",
                    "valorParametro": 432,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "3a73359e-b3ef-d50f-fdf4-5ec6214c4ef2",
                    "valorParametro": 312,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7c2cd323-6061-5d88-1d72-e87a3ac12884",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7da044b9-91a0-206f-50cd-6fb7d53961a9",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a086651b-e113-982a-6de5-c433a8c8c63b",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "8dc29c28-0dc9-04fd-6d15-f70f602da30a",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "06b795f9-c324-cbbb-f13e-f5a3a84cf99f",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "4a622a13-cc83-a3a5-165b-4138cb0a5cf4",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1ce35d43-8881-0e29-5951-6d3c9943cb6f",
                    "valorParametro": 456,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d925ef73-ba47-9b40-75bb-d6a4d325ff2e",
                    "valorParametro": 288,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "0f72d9f2-2880-9480-8127-08c1113662fa",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "3df9b62c-749d-3489-fa3e-2ddd3bb9885d",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "eb2d0932-28df-c94d-88da-6bc4d568d1bd",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "bc6e13f3-9276-2960-f5f0-68211231ea3f",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "aac7f29f-3e07-d4ca-f63c-06f7dbabf389",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "3141ab2e-600b-c0f2-d42b-ff88b5d76650",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "de285bd2-5370-96fe-4c3a-2c1854ee79ee",
                    "valorParametro": 48,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "0cee6ef4-7605-e4c6-606b-92674f93b412",
                    "valorParametro": 648,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "eaf25681-ff52-6285-24d5-3a4932a9c07b",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "af41549f-3f8c-3341-97ee-fbdd8b8b7110",
                    "valorParametro": 48,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d4b47407-5caf-0922-487a-9947b68e5cb1",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "fbb6bb16-f32b-9521-f57f-b87c99eb3944",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "5ab71fc0-2025-9d8f-9f90-bcc4576ebb8f",
                    "valorParametro": 24,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "510d5498-f070-98b8-04ae-a2620d8fdbdd",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "40381603-2f4c-c0f0-8923-546cf5b56635",
                    "valorParametro": 624,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a4f65da8-46da-a9c1-12c6-6f2cb4ac6a2e",
                    "valorParametro": 96,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d2ad6c4b-ca85-b428-5401-74db19675411",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "3bb45a6e-8bb1-f155-19a4-0f09135e2d33",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "252a07e4-f863-9ee1-852c-38f61400c46b",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ef3afaff-61e3-1acc-523b-451e54e6fc17",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "61b045e2-3665-d2ec-6243-e483ae927e9d",
                    "valorParametro": 744,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ee1fa5b6-97d2-e894-3003-5a7eb73ffdb9",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "de554979-8111-1351-b16a-64b33b239822",
                    "valorParametro": 0,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "93663c6c-ef9d-451a-3138-00038e4ae91e",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9aa31984-6793-7346-4ac3-dfec99018dba",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "690e8063-6a33-8c89-56e2-9e0e2a043a00",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "aabfc82a-5db2-6316-4748-595ad7d76bae",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "34927c11-24d8-4cf9-2851-0055e47df7cc",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "13b0e097-5b1b-9f03-c034-6fa9d636f946",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "0e7a14d3-37a3-6e7c-d4d8-68d3c6624d98",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1a3193c4-f557-67e0-2fd7-9d526f052930",
                    "valorParametro": 744,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "bc4ba88b-43d8-d6b9-3511-c6316f0a2332",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "6e5c9ad8-12bf-73c4-0939-e8d80517dc96",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1b7a3cab-58e9-a833-b500-0d7a142810dc",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "00bb0ffc-8e0d-eec2-41cf-7b94871fb1fe",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "8b89df55-d698-aaaa-591f-f5dee5ea790e",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a5b9c74c-bd37-54b1-8fe4-821f18703d7a",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "cfaf87e3-8d95-6767-ae9f-5fb278d52e40",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "34ee1ce9-6d0f-0427-8711-2483d335ff2f",
                    "valorParametro": 432,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "62915c8c-2e81-b23e-6212-94bdb167a165",
                    "valorParametro": 312,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "fff71d4b-db2b-9c7a-15fd-6bbc5efd2f57",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "06565286-ecbd-8496-2681-c9a0f496f767",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "09317df1-6d3e-395e-ed2c-c8cf0d92c58d",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f898bed8-8782-0d33-d8f4-73995b2ea654",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "96304c1b-26de-261c-bbd0-d5c750430191",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7d588d53-bdb8-6784-cb92-a31207135ee4",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f72a9f83-5daa-ee13-cd45-8e807afebe66",
                    "valorParametro": 456,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d163dc46-d143-3f97-a511-e4632786ed88",
                    "valorParametro": 288,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "bd2ee9aa-52e1-7016-5dd6-e06efea5a5aa",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "807a1207-ddb7-92b9-f773-d43abd0ce607",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d713dc7a-8f16-8633-4557-4df19a6c0f25",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1e55eb15-d5dc-896a-211e-693009f00f2c",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "5ef72486-82d1-346a-36bf-b88af05b3537",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "3f7c5e68-eaa6-aee7-1a18-f7e31bd750d0",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "b93c16c5-c0dd-9b2a-305b-f41d445d2a0f",
                    "valorParametro": 48,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "b0544d77-b53d-4f3a-77fb-f223be10ee6d",
                    "valorParametro": 648,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "4328de27-ee32-7182-ac7b-4f2c821d7f41",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "71ecfc5b-340d-6fbd-0fb4-29faa7e66cf3",
                    "valorParametro": 48,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "587caba9-0929-51a9-72d0-b29fbf5577d5",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "b2312fed-96a7-3957-c0cb-ec733aafbf3c",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c6222de2-b8c3-ccc1-e4e6-a5dc675adf60",
                    "valorParametro": 24,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "8337d2f1-2c05-3446-1663-55b9619ea203",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ee8fa954-5aef-3508-f688-e48a4ae0ba7e",
                    "valorParametro": 624,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "47b0ffd4-1e5f-d5fa-b497-b810d054600c",
                    "valorParametro": 96,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a159ee0b-4383-8b28-41f7-0c41a467a9dc",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "dbfb4945-3dfd-f546-af1d-339f19bc9a64",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a5204d43-543b-7ff5-b923-c2cded264133",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "fd971419-dd12-e973-409e-ca35256e5aaf",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "972ce595-9362-8b39-f1bd-cef8303511b4",
                    "valorParametro": 744,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "064ab887-cd74-0037-b1b2-4d89c171e8d9",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "91e4419f-0811-4507-036c-c1fc3b4e5610",
                    "valorParametro": 0,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "912a42fa-c46f-5751-8721-239bfe89e13c",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "55d74f0c-2014-1c02-523a-c1cbd02b8813",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9783600c-7003-7ba7-763a-0c8fcc3bd5e5",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "34c56d4b-7b89-ebba-7c49-3f072ad94975",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "98688ae6-68ef-5e38-dff2-92c60bd88b21",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "e9bef461-2c7d-7dec-e782-f81d8846eb74",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "480bd75f-38f0-fd4a-07c9-a8fdcc35157f",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "35ed060e-6f93-24e8-39d7-ed0355cab97e",
                    "valorParametro": 744,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "8fe1c55b-df10-1304-1838-b8f71fd46545",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a2983be0-7861-b63f-e2ec-57a6c2b36785",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "203f2e43-0e4a-f860-d3e1-731d8a00a35b",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "8fd0fb17-3047-2dae-1560-11eb586d795d",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f5791d36-c674-1c3e-5590-79dcb31af04d",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "71196658-7b30-f377-9d97-d8a377dd81c8",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "4b679a82-1b28-91bd-049e-cbc0ac38a503",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f4b12788-659d-ab8b-079e-debabc1ac58c",
                    "valorParametro": 432,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "2727497b-c3ba-fb20-32ec-a091a2bc691d",
                    "valorParametro": 312,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9fcc54c0-f7ed-1653-a446-da325192065a",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "0761fbe6-3388-148c-c5db-894e8c481608",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "01a24e5c-c007-39e8-c04c-ac29a3b2037a",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f134eb10-7451-d914-0069-a36930a38c2f",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9de05060-1aca-a7d6-0808-cfd21e5da338",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "3398170d-14cc-dc7a-2a36-56eabbfb10de",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "762bc27f-4764-eba5-30dc-6292c8c4f7b8",
                    "valorParametro": 456,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "538bac05-79b9-6182-274d-c69cf568a74c",
                    "valorParametro": 288,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "2c1ca6c9-f7a8-910b-9554-c486650a4a6d",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "bd26efd9-6540-84a8-48bf-fd13189e8bad",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "262419c1-ec67-4bd2-213a-e3d0ecc8e5d1",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7470ebb9-f1aa-1d24-0502-654faac6bb30",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "717dc98e-21ee-8689-3682-7b908dea1760",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c7c4db8e-0d3f-9094-85a5-22e1ea2ab3e9",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1f7acd0e-77d2-337d-f3b3-384945e157a3",
                    "valorParametro": 48,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "b22fb198-7d84-6c2d-8409-512a4fed8ea7",
                    "valorParametro": 648,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "bd9bc263-ffaf-af58-e744-8e71748073f3",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a4004db1-c72f-3d89-6bde-cbfe07f6a2f6",
                    "valorParametro": 48,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "8dcfd6bd-60f2-1364-0e22-43270b6fc136",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "b5dae424-a22c-86ed-db08-43ebbe831a0e",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "b795b758-776c-18b9-b9d3-d603e02a589b",
                    "valorParametro": 24,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "dfbb9fee-db69-1281-7e40-4ec97d24e379",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a3f7cfe9-b55c-0bee-9b12-f3688b764455",
                    "valorParametro": 624,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "6f9f009f-c546-4819-7b1f-ecfec552af92",
                    "valorParametro": 96,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "478674d6-6e6b-63c4-047e-8a2dcb6d3fd1",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "506d4977-2988-0143-ef0e-f589ec36aa4a",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "61a1854c-cffc-895b-e673-60cffec95ccf",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f6203414-c881-f26e-3096-439a0e5911c6",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG1",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "1573e2fa-0ee2-ba04-4e6b-80be21bbcc00",
                    "valorParametro": 744,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "5bc345b2-7954-51ea-b762-f54652db718e",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "72b00e22-47ea-c01c-9f13-4a51880cdb6e",
                    "valorParametro": 0,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "0af5691b-d0de-909a-807a-f90ac71a646a",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7cc58c94-9be9-f4f7-6648-bee72561060a",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "12a3c040-5ffb-5afe-b64b-69840748c955",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "cb47e6c3-fcb5-15ae-364d-a9e6f6c20af3",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9203112d-81ab-2e9c-4825-f208c849e770",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG2",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9c0fe189-44f3-1f35-c78b-c549bf6cc589",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "39f186c7-1ce9-c157-1e65-e11594d05335",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "23617c86-8ff4-5614-fdce-a1def831b3c7",
                    "valorParametro": 744,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "01a335c4-96c0-f701-126e-a466297d9f0d",
                    "valorParametro": 0,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "4679a4c2-0c71-d4d7-af96-022b6e687102",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "5423fa49-66e6-922a-c916-3b9543c220bc",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "96d8d338-3a3b-ea45-8ea6-28bd231b3039",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9d4d3484-e0c3-a091-aad7-7488bcbe7d0b",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG3",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "c1bea06f-1175-e71a-af84-880c5995cc25",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9f2d8cf5-5824-a2bb-b94c-ec098e2cd69e",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "192ad75d-09d8-3c27-a0f3-b7f4a3f2503a",
                    "valorParametro": 432,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "28c6a659-0ec7-ec4d-fd98-8462980bb9b4",
                    "valorParametro": 312,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "002ac5c2-9398-7e67-f660-60e7ebd8bdc9",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "227a2d82-48aa-90a9-4234-8f9214ec4063",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "11933656-1540-89fc-972d-18bf2308236d",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ec0adeef-c78d-b649-581d-baccb43555a7",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG4",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "fc484ecd-cef9-6717-8891-400624108512",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "4def84ef-ab0e-5a3a-229e-d2c0ccee9e12",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "f28b7fac-40e2-b9fe-81a2-cb4d8a5de1c6",
                    "valorParametro": 456,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "3a69f443-386f-51b3-a19b-facc230de398",
                    "valorParametro": 288,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "7ce29f57-1bef-071f-0014-cab03b16cbda",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "879f9202-f422-f023-cfeb-9dbf2eb511ea",
                    "valorParametro": 0,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "4fc96b2f-0da5-2864-8c06-8d369d118090",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "e0bb1fe3-07c3-80b2-1ccd-b274d7249f94",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG5",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "9a46c9a2-04b2-9d38-1391-33c70d870a04",
                    "valorParametro": 0,
                    "idTipoParametro": "HDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "33b0a035-0128-11ce-7d53-a3577e17cab1",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDF",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "34c19b5b-cabd-a005-f272-d92a18b32e02",
                    "valorParametro": 48,
                    "idTipoParametro": "HS",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "a7b35f1c-39b2-ab1f-67b3-9b6cd5a92a34",
                    "valorParametro": 648,
                    "idTipoParametro": "HRD",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "46b79308-7704-9d7b-2e96-b25430c994ff",
                    "valorParametro": 0,
                    "idTipoParametro": "HDCE",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "d44a75a5-7e69-0173-7888-c9d9adeb16e0",
                    "valorParametro": 48,
                    "idTipoParametro": "HDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "ec3628a3-25e4-e641-5088-9280d076bce3",
                    "valorParametro": 0,
                    "idTipoParametro": "HEDP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                },
                {
                    "_metadata": {
                        "type": "parametrotaxa",
                        "changeTrack": "create"
                    },
                    "id": "75720876-43d7-67b5-0f53-813baf249588",
                    "valorParametro": 744,
                    "idTipoParametro": "HP",
                    "idUge": "ALUXG-0UG6",
                    "idFechamento": "8245c512-bfcc-f1ff-2a2d-a844ddf5a02f",
                    "idExecucaoCalculoFechamento": "a2b81623-fec2-689a-0c5c-e5610505ea1c",
                    "mes": 10,
                    "ano": 2014
                }
            ]
        }
    }
}
    """
    r = json.loads(r)
    res.data = r
    return res

# TODO ajustar para o modelo default da aplicacao
#def test_persist_data_from_process_memory(session):
#     with patch.object(HttpClient, 'get', return_value=head_of_process_memory()) as mock_method:
#       p = BatchPersistence(session)
#       p.run("1")