import pandas as pd
import logging

class TRANSFORM_BRELLA_LIST:

    def __init__(self, lists_json: str):
        self.lists_json = lists_json

    def transform_brella_items(self) -> pd.DataFrame:
        try:
            df_item_list = pd.json_normalize(self.lists_json, record_path=["data"])

            if df_item_list.empty:
                logging.error("No data found in Brella Invitation List")
                #Proceed with an empty DataFrame instead of stopping the execution
                return pd.DataFrame()
            
            df_item_list['Name'] = df_item_list['attributes.external-first-name'].str.cat(df_item_list['attributes.external-last-name'],sep=" ")
            df_item_ids = df_item_list.loc[:,["attributes.qr-string",'Name',"attributes.external-company","attributes.external-id",]]
            logging.info("Successfully transformed invitation info into Dataframe")
            return df_item_ids
        
        except Exception as e:
            logging.error(f"Error creating DataFrame: {e}")
            return None
    
    def transform_brella_qr(self):
        try:
            df_item_list = pd.json_normalize(self.lists_json, record_path=["data"])

            if df_item_list.empty:
                logging.error("No data found in Brella Invitation List")
                #Proceed with an empty DataFrame instead of stopping the execution
                return pd.DataFrame()
            
            df_item_ids = df_item_list["attributes.qr-string"].tolist()
            logging.info("Successfully transformed invitation info into Dataframe")
            return df_item_ids
        
        except Exception as e:
            logging.error(f"Error creating DataFrame: {e}")
            return None
    