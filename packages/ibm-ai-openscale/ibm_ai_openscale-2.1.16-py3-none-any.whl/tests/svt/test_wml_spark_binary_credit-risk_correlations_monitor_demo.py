
# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from assertions import *
import pandas as pd
from pyspark import SparkContext, SQLContext
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import StringIndexer, VectorAssembler, IndexToString
from pyspark.sql.types import StructType, DoubleType, StringType, ArrayType
from ibm_ai_openscale.utils.href_definitions_v2 import AIHrefDefinitionsV2
from ibm_ai_openscale.utils.inject_demo_data import DemoData
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType


DAYS = 7
RECORDS_PER_DAY = 2880


class TestAIOpenScaleClient(unittest.TestCase):
    hrefs_v2 = None
    log_loss_random = None
    brier_score_loss = None
    application_instance_id = None
    drift_instance_id = None
    data_set_id = None
    ai_client = None
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    b_app_uid = None
    x_uid = None
    labels = None
    corr_monitor_instance_id = None
    variables = None
    wml_client = None
    subscription = None
    binding_uid = None
    aios_model_uid = None
    scoring_result = None
    payload_scoring = None
    published_model_details = None
    monitor_uid = None
    source_uid = None
    correlation_monitor_uid = 'correlations'
    measurement_details = None
    transaction_id = None
    business_payload_records = 0
    drift_model_name = "drift_detection_model.tar.gz"
    drift_model_path = os.path.join(os.getcwd(), 'artifacts', 'drift_models')
    historical_data_path = os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'historical_records')
    data_df = pd.read_csv(
        "./datasets/German_credit_risk/credit_risk_training.csv",
        dtype={'LoanDuration': int, 'LoanAmount': int, 'InstallmentPercent': int, 'CurrentResidenceDuration': int,
               'Age': int, 'ExistingCreditsCount': int, 'Dependents': int})

    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.hrefs_v2 = AIHrefDefinitionsV2(cls.aios_credentials)
        cls.database_credentials = get_database_credentials()
        cls.hd = DemoData(cls.aios_credentials)
        cls.database_credentials = get_database_credentials()

        if "ICP" in get_env():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
            upload_credit_risk_training_data_to_db2(cls.database_credentials)

        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

        prepare_env(cls.ai_client)

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_03_bind_wml_instance(self):
        if "ICP" in get_env():
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on ICP", WatsonMachineLearningInstance4ICP())
        else:
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on Cloud", WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        print("Binding details:\n{}".format(self.ai_client.data_mart.bindings.get_details(self.binding_uid)))

        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)

    def test_05_prepare_model(self):
        asset_name = "AIOS Spark German Risk model drift"
        deployment_name = "AIOS Spark German Risk deployment drift"

        TestAIOpenScaleClient.model_uid, TestAIOpenScaleClient.deployment_uid = get_wml_model_and_deployment_id(
            model_name=asset_name, deployment_name=deployment_name)

        if self.deployment_uid is None:
            ctx = SparkContext.getOrCreate()
            sc = SQLContext(ctx)

            spark_df = sc.read.format("com.databricks.spark.csv").option("header", "true").option("delimiter", ",").option("inferSchema", "true").load(
                os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'credit_risk_training.csv'))
            spark_df.printSchema()

            (train_data, test_data) = spark_df.randomSplit([0.8, 0.2], 24)
            print("Number of records for training: " + str(train_data.count()))
            print("Number of records for evaluation: " + str(test_data.count()))

            si_CheckingStatus = StringIndexer(inputCol='CheckingStatus', outputCol='CheckingStatus_IX')
            si_CreditHistory = StringIndexer(inputCol='CreditHistory', outputCol='CreditHistory_IX')
            si_LoanPurpose = StringIndexer(inputCol='LoanPurpose', outputCol='LoanPurpose_IX')
            si_ExistingSavings = StringIndexer(inputCol='ExistingSavings', outputCol='ExistingSavings_IX')
            si_EmploymentDuration = StringIndexer(inputCol='EmploymentDuration', outputCol='EmploymentDuration_IX')
            si_Sex = StringIndexer(inputCol='Sex', outputCol='Sex_IX')
            si_OthersOnLoan = StringIndexer(inputCol='OthersOnLoan', outputCol='OthersOnLoan_IX')
            si_OwnsProperty = StringIndexer(inputCol='OwnsProperty', outputCol='OwnsProperty_IX')
            si_InstallmentPlans = StringIndexer(inputCol='InstallmentPlans', outputCol='InstallmentPlans_IX')
            si_Housing = StringIndexer(inputCol='Housing', outputCol='Housing_IX')
            si_Job = StringIndexer(inputCol='Job', outputCol='Job_IX')
            si_Telephone = StringIndexer(inputCol='Telephone', outputCol='Telephone_IX')
            si_ForeignWorker = StringIndexer(inputCol='ForeignWorker', outputCol='ForeignWorker_IX')
            si_Label = StringIndexer(inputCol="Risk", outputCol="label").fit(spark_df)
            label_converter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=si_Label.labels)

            va_features = VectorAssembler(
                inputCols=["CheckingStatus_IX", "CreditHistory_IX", "LoanPurpose_IX", "ExistingSavings_IX",
                           "EmploymentDuration_IX", "Sex_IX", "OthersOnLoan_IX", "OwnsProperty_IX", "InstallmentPlans_IX",
                           "Housing_IX", "Job_IX", "Telephone_IX", "ForeignWorker_IX", "LoanDuration", "LoanAmount",
                           "InstallmentPercent", "CurrentResidenceDuration", "LoanDuration", "Age", "ExistingCreditsCount",
                           "Dependents"], outputCol="features")

            classifier = RandomForestClassifier(featuresCol="features")

            pipeline = Pipeline(
                stages=[si_CheckingStatus, si_CreditHistory, si_EmploymentDuration, si_ExistingSavings, si_ForeignWorker,
                        si_Housing, si_InstallmentPlans, si_Job, si_LoanPurpose, si_OthersOnLoan,
                        si_OwnsProperty, si_Sex, si_Telephone, si_Label, va_features, classifier, label_converter])

            model = pipeline.fit(train_data)
            predictions = model.transform(test_data)
            evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction")
            auc = evaluator.evaluate(predictions)

            print("Accuracy = %g" % auc)

            train_data_schema = spark_df.schema
            label_field = next(f for f in train_data_schema.fields if f.name == "Risk")
            label_field.metadata['values'] = si_Label.labels
            input_fileds = filter(lambda f: f.name != "Risk", train_data_schema.fields)

            output_data_schema = StructType(list(input_fileds)). \
                add("prediction", DoubleType(), True, {'modeling_role': 'prediction'}). \
                add("predictedLabel", StringType(), True,
                    {'modeling_role': 'decoded-target', 'values': si_Label.labels}). \
                add("probability", ArrayType(DoubleType()), True, {'modeling_role': 'probability'})

            if "ICP" in get_env():
                training_data_reference = {
                    "name": "Credit Risk feedback",
                    "connection": self.database_credentials,
                    "source": {
                        "tablename": "CREDIT_RISK_TRAINING",
                        'schema_name': 'TRAININGDATA',
                        "type": "db2"
                    }
                }
            else:
                db2_credentials = {
                    "hostname": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
                    "password": "89TsmoAN_Sb_",
                    "https_url": "https://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:8443",
                    "port": 50000,
                    "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;Security=SSL;",
                    "host": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
                    "jdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
                    "uri": "db2://dash14647:89TsmoAN_Sb_@dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
                    "db": "BLUDB",
                    "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;",
                    "username": "dash14647",
                    "ssljdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50001/BLUDB:sslConnection=true;"
                }

                training_data_reference = {
                    "name": "Credit Risk feedback",
                    "connection": db2_credentials,
                    "source": {
                        "tablename": "CREDIT_RISK_TRAINING",
                        "type": "dashdb"
                    }
                }

            print("Training data reference:\n{}".format(training_data_reference))

            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(asset_name),
                self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: training_data_reference,
                self.wml_client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA: output_data_schema.jsonValue(),
                self.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                    {
                        "name": "AUC",
                        "value": auc,
                        "threshold": 0.8
                    }
                ]
            }

            print("Publishing a new model...")
            published_model_details = self.wml_client.repository.store_model(model=model, meta_props=model_props, training_data=train_data, pipeline=pipeline)

            print("Published model details:\n{}".format(published_model_details))
            TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model_details)

            print("Deploying model: {}, deployment name: {}".format(asset_name, deployment_name))
            deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name=deployment_name, asynchronous=False)
            TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)

            deployment_details = self.wml_client.deployments.get_details(self.deployment_uid)
            print("Deployment details:\n{}".format(deployment_details))

    def test_06_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(
            source_uid=TestAIOpenScaleClient.model_uid,
            binding_uid=self.binding_uid,
            problem_type=ProblemType.BINARY_CLASSIFICATION,
            input_data_type=InputDataType.STRUCTURED,
            prediction_column='predictedLabel',
            probability_column='probability',
            feature_columns=['CheckingStatus', 'LoanDuration', 'CreditHistory', 'LoanPurpose', 'LoanAmount',
                             'ExistingSavings', 'EmploymentDuration', 'InstallmentPercent', 'Sex', 'OthersOnLoan',
                             'CurrentResidenceDuration', 'OwnsProperty', 'Age', 'InstallmentPlans', 'Housing',
                             'ExistingCreditsCount', 'Job', 'Dependents', 'Telephone', 'ForeignWorker'],
            categorical_columns=['CheckingStatus', 'CreditHistory', 'LoanPurpose', 'ExistingSavings',
                                 'EmploymentDuration', 'Sex', 'OthersOnLoan', 'OwnsProperty', 'InstallmentPlans',
                                 'Housing', 'Job', 'Telephone', 'ForeignWorker']
        ))

        # WORKAROUND FOR #8237 issue
        if "ICP" in get_env():
            db_cr = self.database_credentials
            db_cr['database_name'] = self.database_credentials['db']
            db_cr['connection_string'] = self.database_credentials['jdbcurl']

            tdr = {
                'type': 'db2',
                "name": "Credit Risk feedback",
                "connection": db_cr,
                "location": {
                    "tablename": "CREDIT_RISK_TRAINING",
                    "schema_name": "TRAININGDATA",
                }
            }

            subscription.update(training_data_reference=tdr)

        TestAIOpenScaleClient.subscription_uid = subscription.uid

        print("Subscription details: {}".format(subscription.get_details()))

    def test_07_select_subscription(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)

    def test_08_a_load_historical_scoring_payload(self):
        self.hd.load_historical_scoring_payload(TestAIOpenScaleClient.subscription, TestAIOpenScaleClient.deployment_uid, TestAIOpenScaleClient.historical_data_path)

    def test_08_b_stats_on_payload_logging_table(self):
        wait_for_payload_table(subscription=self.subscription, payload_records=RECORDS_PER_DAY*DAYS)

        TestAIOpenScaleClient.subscription.payload_logging.show_table(limit=5)
        records_no = TestAIOpenScaleClient.subscription.payload_logging.get_records_count()
        print("Rows count in payload logging table", records_no)

        print('Subscription details: ', TestAIOpenScaleClient.subscription.get_details())

    def test_09_define_business_app(self):
        payload = {
            "name": "Credit Risk Application",
            "description": "Test Business Application",
                "payload_fields": [
                    {
                        "name": "LoanDuration",
                        "type": "number",
                    },
                    {
                        "name": "LoanPurpose",
                        "type": "string",
                    },
                    {
                        "name": "LoanAmount",
                        "type": "number",
                    },
                    {
                        "name": "InstallmentPercent",
                        "type": "number",
                    },
                    {
                        "name": "AcceptedPercent",
                        "type": "number",
                    },
                     {
                        "name": "Accepted",
                        "type": "number",
                    },
                    {
                        "name": "AmountGranted",
                        "type": "number",
                    }
                ],
            "business_metrics": [
                {
                    "name": "Accepted Credits",
                    "description": "Accepted Credits Daily",
                    "expected_direction": "increasing",
                    "thresholds": [
                        {
                            "type": "lower_limit",
                            "default": 502,
                            "default_recommendation": "string"
                        }
                    ],
                    "required": False,
                    "calculation_metadata": {
                        "field_name": "Accepted",
                        "aggregation": "avg",
                        "time_frame": {
                            "count": 1,
                            "unit": "day"
                        }
                    }
                },
                {
                    "name": "Credit Amount Granted",
                    "description": "Credit Amount Granted Daily",
                    "expected_direction": "increasing",
                    "thresholds": [
                        {
                            "type": "lower_limit",
                            "default": 1000,
                            "default_recommendation": "string"
                        }
                    ],
                    "required": False,
                    "calculation_metadata": {
                        "field_name": "AmountGranted",
                        "aggregation": "sum",
                        "time_frame": {
                            "count": 1,
                            "unit": "day"
                        }
                    }
                }
            ],
            "subscription_ids": [
                TestAIOpenScaleClient.subscription_uid
            ],
        }

        response = requests.post(url=self.hrefs_v2.get_applications_href(),
                                 headers=TestAIOpenScaleClient.ai_client._get_headers(), json=payload)
        print(response.status_code, response.json())
        self.assertEqual(response.status_code, 202)
        TestAIOpenScaleClient.b_app_uid = response.json()['metadata']['id']
        self.assertIsNotNone(TestAIOpenScaleClient.b_app_uid)

    def test_10_get_application_details(self):
        application_details = wait_for_business_app(url_get_details=self.hrefs_v2.get_application_details_href(TestAIOpenScaleClient.b_app_uid),
                                 headers=TestAIOpenScaleClient.ai_client._get_headers())
        print(application_details)

    def test_11_enable_drift(self):
        self.subscription.drift_monitoring.enable(threshold=0.6, min_records=10, model_path=os.path.join(self.drift_model_path, self.drift_model_name))
        drift_monitor_details = self.subscription.monitoring.get_details(monitor_uid='drift')
        print('drift monitor details', drift_monitor_details)

    def test_12_list_monitors_instances(self):
        self.ai_client.data_mart.monitors.list()
        time.sleep(5)
        response = requests.get(url=self.hrefs_v2.get_monitor_instances_href(), headers=self.ai_client._get_headers())
        print(response.json())
        instances = response.json()['monitor_instances']

        for instance in instances:
            if 'managed_by' in instance['entity'] and instance['entity']['managed_by'] == self.b_app_uid:
                TestAIOpenScaleClient.application_instance_id = instance['metadata']['id']

            if instance['entity']['monitor_definition_id'] == 'correlations':
                TestAIOpenScaleClient.corr_monitor_instance_id = instance['metadata']['id']

            if instance['entity']['monitor_definition_id'] == 'drift':
                TestAIOpenScaleClient.drift_instance_id = instance['metadata']['id']

        self.assertIsNotNone(TestAIOpenScaleClient.application_instance_id)
        self.assertIsNotNone(TestAIOpenScaleClient.corr_monitor_instance_id)
        self.assertIsNotNone(TestAIOpenScaleClient.drift_instance_id)
        print('application_instance_id', self.application_instance_id)
        print('corr_monitor_instance_id', self.corr_monitor_instance_id)
        print('drift_instance_id', self.drift_instance_id)

    def test_13_get_business_payload_data_set_details(self):
        response = requests.get(url=self.hrefs_v2.get_data_sets_href(), headers=self.ai_client._get_headers())
        data_sets = response.json()['data_sets']
        TestAIOpenScaleClient.data_set_id = [ds['metadata']['id'] for ds in data_sets if ds['entity']['type']=='business_payload'][0]
        print("business_payload data_set id: {}".format(TestAIOpenScaleClient.data_set_id))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(TestAIOpenScaleClient.data_set_id)
        print(response.json())

    def test_14_insert_business_payload(self):
        self.hd.load_historical_business_payload(
            file_path=TestAIOpenScaleClient.historical_data_path,
            data_set_id=TestAIOpenScaleClient.data_set_id
        )
        TestAIOpenScaleClient.business_payload_records = RECORDS_PER_DAY*DAYS

    def test_15_stats_on_business_payload_data(self):
        business_records = wait_for_records_in_data_set(
            url_get_data_set_records=self.hrefs_v2.get_data_set_records_href(TestAIOpenScaleClient.data_set_id),
            headers=self.ai_client._get_headers(),
            data_set_records=self.business_payload_records,
            waiting_timeout=180
        )
        # self.assertEqual(business_records, self.business_payload_records)

    def test_16_load_historical_bkpis(self):
        self.hd.load_historical_kpi_measurements(
            file_path=TestAIOpenScaleClient.historical_data_path,
            monitor_instance_id=self.application_instance_id,
        )

    def test_17_get_historical_kpi(self):
        query = '?start=2018-01-23T12:46:55.677590Z&end=2019-12-04T12:46:55.677590Z&limit=1000'
        metrics_url = self.hrefs_v2.get_measurements_href(self.application_instance_id) + query
        response = requests.get(url=metrics_url, headers=self.ai_client._get_headers())

        self.assertEqual(200, response.status_code)
        print(response.json())
        print(response.json()['measurements'][0])

    def test_18_a_store_drift_measurements(self):
        self.hd.load_historical_drift_measurements(
            file_path=TestAIOpenScaleClient.historical_data_path,
            monitor_instance_id=self.drift_instance_id,
            business_application_id=self.b_app_uid)

    def test_18b_get_drift_measurements(self):
        query = '?start=2018-01-23T12:46:55.677590Z&end=2019-12-04T12:46:55.677590Z'
        metrics_url = self.hrefs_v2.get_measurements_href(self.drift_instance_id) + query
        response = requests.get(url=metrics_url, headers=self.ai_client._get_headers())

        self.assertEqual(200, response.status_code)
        print(response.json()['measurements'][0])

    def test_19_run_correlation_monitor(self):
        time.sleep(30)

        payload = {
            "triggered_by": "user",
            "parameters": {
                "max_number_of_days": "1000"
            },
            "business_metric_context": {
                "business_application_id": TestAIOpenScaleClient.b_app_uid,
                "metric_id": "avg_revenue",
                "transaction_data_set_id": "",
                "transaction_batch_id": ""
            }
        }

        response = requests.post(
            url=self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.corr_monitor_instance_id),
            json=payload,
            headers=TestAIOpenScaleClient.ai_client._get_headers())

        print(response.json())
        self.assertEqual(response.status_code, 201)
        TestAIOpenScaleClient.correlation_run_id = response.json()['metadata']['id']

    def test_22_check_correlations_metrics(self):
        run_url = self.hrefs_v2.get_monitor_instance_run_href(TestAIOpenScaleClient.corr_monitor_instance_id)+"/"+self.correlation_run_id
        print(run_url)
        final_run_details = wait_for_monitor_instance(run_url, headers=self.ai_client._get_headers())
        self.assertIsNot(final_run_details['entity']['status']['state'], 'error',
                         msg="Error during computing correlations. Run details: {}".format(final_run_details))

        query = '?start=2018-01-23T12:46:55.677590Z&end=2019-12-04T12:46:55.677590Z'
        url = self.hrefs_v2.get_measurements_href(TestAIOpenScaleClient.corr_monitor_instance_id) + query
        print(url)
        print(final_run_details)

        response = requests.get(url=url, headers=self.ai_client._get_headers())

        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('significant_coefficients' in str(response.json()))

        corr_metrics = response.json()['measurements'][0]['entity']['values'][0]['metrics']
        self.assertGreater([metric['value'] for metric in corr_metrics if metric['id'] == 'significant_coefficients'][0], 0,
                           msg="No significant coefficients")

    def test_34_unsubscribe(self):
        self.ai_client.data_mart.subscriptions.delete(self.subscription.uid)

    def test_35_unbind(self):
        self.ai_client.data_mart.bindings.delete(self.binding_uid)

    @classmethod
    def tearDownClass(cls):
        print("Deleting DataMart.")
        cls.ai_client.data_mart.delete()


if __name__ == '__main__':
    unittest.main()
