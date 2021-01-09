import pandas as pd 
import numpy as np
import networkx as nx
import os
from datetime import datetime

data_path = 'C:/Users/Kinga/OneDrive/thesis/data/cbm/200703_company_list_DB.xlsx'

class Utils():
    def __init__(self):
        pass
    def cols2unique(self, df, columns):
        '''
        Gets values from columns, puts them together and returns an array of unique values
        '''
        assert type(df)==pd.DataFrame
        columns_locs = []
        for column in columns:
            columns_locs.append(pd.Series(df[column]))
        locs = pd.concat(columns_locs)
        unique_array = locs.unique()
        return unique_array

class GraphUtils(Utils):
    def init_graph(self, node_names):
        G = nx.DiGraph() #change to MultiDiGraph
        for node in node_names:
            G.add_node(node)
        return G

    def get_nodes(self):
        return self.cols2unique(self.df, columns=['ac_location','mc_location'])

class Data(GraphUtils):
    def __init__(self):
        self.raw_df = pd.read_excel(data_path)
        self.df = self.preprocess(self.raw_df)
        self.countries =    ['Germany', 'Luxembourg', 'Netherlands', 'Italy', 'United Kingdom',
                            'France', 'Austria', 'Sweden', 'Finland', 'Cyprus', 'Belgium',
                            'Ireland', 'Denmark', 'Estonia', 'Norway', 'Czech Republic', 'Latvia',
                            'Poland', 'Spain', 'Slovakia', 'Malta', 'Romania', 'Lithuania',
                            'Croatia', 'Hungary', 'Bulgaria', 'Switzerland']
        
    
    def preprocess(self, df):
        ''' Static '''
        df = df[df['type']=='CBM']
        df = df[['ct_id', 'date', 'ac_location','mc_location','name', 'parent_name', 'mc_name']]
        df = df.dropna(axis = 0, how='any')
        return df

    def df2graph(self, start_date=datetime(2007, 12, 5), end_date=datetime(2019, 12, 5)):
        """Hybrid"""
        df = self.df
        # create a dictionary containing edges and their data
        #TODO: generalize to df2graph?
        countries = self.countries
        G = self.init_graph(countries)
        assert len(countries)>1
        t_date = []
        t_from = []
        t_to = []
        country_links = {country:{country:0 for country in countries} for country in countries}
        country_links
        done_transactions = []
        for row_id in df.index:

            transaction_id = df.at[row_id, 'ct_id']
            transaction_date = df.at[row_id, 'date']
            #transaction_date = datetime.strptime(transaction_date, '%Y-%m-%d')
            if transaction_date>start_date and transaction_date<end_date:
                n1 = df.at[row_id, 'mc_location']
                n2 = df.at[row_id, 'ac_location']
                if [n1,n2,transaction_id] not in done_transactions:
                    if n1 in countries and n2 in countries:
                        done_transactions.append([n1,n2,transaction_id])
                        country_links[n1][n2]+=1
                        t_date.append(transaction_date)
                        t_from.append(n1)
                        t_to.append(n2)
                else:
                    continue
        # populate edges from a dictionary
        for n1 in country_links:
            for n2 in country_links[n1]:
                weight = country_links[n1][n2]
                if weight>0:
                    G.add_edge(n1, n2, weight = weight, label = int(weight))
        transactions = [t_date, t_from, t_to]
        self.graph = G
        return G

    def sum_edges_for_nodes(self, method):
        nodes = self.countries
        total_list = []
        for country in nodes:
            out = method(country, data=True)
            total = 0
            for edge in out:
                #print(edge)
                total+=edge[2]['weight']
            total_list.append(total)
        return total_list

    def get_centralities(self):
        # ! assumes yearly centrality score
        all_years_centralities = []

        for y in range(2007,2019):
            start_date = datetime(y, 1, 1)
            end_date = datetime(y+1, 1, 1)
            G = self.cbcm2graph(start_date=start_date, end_date=end_date)

            df0 = pd.DataFrame.from_dict(dict(G.degree()), orient = 'index', columns=['DEG'])
            df1 = pd.DataFrame.from_dict(dict(nx.pagerank(G,weight=0)), orient = 'index', columns=['PR'])
            df2 = pd.DataFrame.from_dict(dict(nx.pagerank(G,weight='weight')), orient = 'index', columns=['PRW'])
            df_all = pd.concat([df0, df1, df2], axis = 1)
            dff_all = df_all.sort_values(by='PRW',axis='index', ascending =False)
            #print(y, '\n', dff_all.head(), '\n')
            '''
            # compute various centralities
            methods = {
                    'Degree':nx.degree_centrality, 
                    'IN degree':nx.in_degree_centrality, 
                    'OUT degree':nx.out_degree_centrality,
                'Page Rank': nx.pagerank, 
                    ##'eigenvector_centrality':nx.eigenvector_centrality,
                        ##'katz_centrality':nx.katz_centrality
                    #'closeness_centrality':nx.closeness_centrality,
                    ##'current_flow_closeness_centrality':nx.current_flow_closeness_centrality,
                    #'betweenness_centrality':nx.betweenness_centrality,
                    #'harmonic_centrality':nx.harmonic_centrality,
                    ##'voterank':nx.voterank           
                    }
            series_dict = {method_name:methods[method_name](G) for method_name in methods.keys()}
            df_scores = pd.DataFrame(series_dict)
            #df_transactions = pd.DataFrame.from_dict(dict(G.degree()), orient = 'index', columns=['# connections'])
            df_degrees = pd.DataFrame.from_dict(dict(G.degree()), orient = 'index', columns=['# connections'])
            df_all = pd.concat([df_degrees, df_scores], axis = 1, sort=False)
            df_all = df_all.sort_values(by='Degree',axis='index', ascending =False)
            '''
            all_years_centralities.append(dff_all)
        return all_years_centralities
    def edges2dict(self, G):
        """ static"""
        from collections import defaultdict
        import itertools
        f = itertools.permutations(list(G.nodes()),2)
        weights =[]
        edge_data = defaultdict()
        for e in f:
            edge_data[e]=0
        dummy = edge_data.copy()
        for edge in G.edges:
            test = edge in dummy.keys()
            if test==False:
                print('Key not in defaultdict!!!!', edge)
            d = G.get_edge_data(*edge)
            edge_data[edge]=d['weight']
        return edge_data

data = Data()