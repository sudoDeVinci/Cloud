# Sort dictionaries for easier separating later
from gc import collect


sorted_bgr_dict = sorted(bgr_dict)
bgr_dict = {key:bgr_dict[key] for key in sorted_bgr_dict}
bgr_indexes = list(bgr_dict.keys())

cloud_final = "c"+str(cloud_bgr_num).zfill(5)
sky_final = 's'+str(sky_bgr_num-2).zfill(5)

# Show pixels counts
print(f" └ {cloud_bgr_num} cloud pixels")
print(f" └ {sky_bgr_num} sky pixels")
print("\n")

del sorted_bgr_dict
collect()

print("Creating BGR dataframe ...")
bgr_df = pd.DataFrame(bgr_dict, index = ['b','g','r'])
bgr_df = bgr_df.apply(pd.to_numeric)
bgr_df = bgr_df.T
print("\n")

""" Now we scale our bgr and hsv values"""
print("Scaling and fitting Data ...")
scaled_bgr = preprocessing.scale(bgr_df)

"""Now we fit both our datasets"""
bgr_pca = PCA()
bgr_pca.fit(scaled_bgr)
print("\n")

"""Now we generate our coordinates for PCA Graph"""
print("Generating Graph Data ...")
bgr_pca_data = bgr_pca.transform(scaled_bgr)

"""At this point we don't need the original dataframes"""
del scaled_bgr
del bgr_df
del bgr_dict
collect()
print("\n")

"""Calculate variance and labels"""
print("Creating BGR Screeplot ...")
bgr_per_var = np.round(bgr_pca.explained_variance_ratio_*100, decimals=1)
bgr_labels = ["PC" + str(i) for i in range(1, len(bgr_per_var)+1)]
plt.bar(x=range(1, len(bgr_per_var)+1), height = bgr_per_var, tick_label = bgr_labels)
plt.ylabel('Variance percentage')
plt.xlabel('Principle component')
plt.title('BGR Scree Plot')
plt.savefig(bgrScreePath)
plt.clf()


"""Create the dataframes we use for our scatterplot"""
bgr_pca_df = pd.DataFrame(bgr_pca_data, index = bgr_indexes, columns = bgr_labels)


del bgr_pca
del bgr_pca_data
del bgr_labels
collect()


"""
Create A scatterplot for our pca data.
First we split our dataframe into two so wee can colour code them
"""

bgr_cloud_df = bgr_pca_df.loc["c00001" : cloud_final, :]
bgr_sky_df = bgr_pca_df.loc["s00001" : sky_final, :]
del bgr_pca_df
collect()

 print("Creating BGR PCA Scatterplot ...")
_,ax = plt.subplots(figsize=(10,6))
ax.scatter(bgr_cloud_df.PC1,bgr_cloud_df.PC2, c = 'lightblue',alpha = 0.4,marker = 'X',label = 'Cloud BGR Value')
ax.scatter(bgr_sky_df.PC1,bgr_sky_df.PC2,c = 'red',alpha = 0.1,marker = 'o',label = 'Sky BGR Value')
plt.legend(loc="upper left")
plt.title('BGR PCA')
plt.xlabel('PC1 - {0}%'.format(bgr_per_var[0]))
plt.ylabel('PC2 - {0}%'.format(bgr_per_var[1]))
plt.savefig(bgrBarPath)
plt.clf

del bgr_cloud_df
del bgr_sky_df
del bgr_per_var
collect()