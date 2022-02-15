# crypto_de_project
Small project to potentially take a look at celebrity participation in cryptocurrency.

**Context:** Cryptocurrency has ballooned in popularity within the past decade and many celebrities have started to participate within the space in some form or way. Supporters of cryptocurrency also proclaim that decentralization and having a public ledger for digital currency are some key attributes that make cryptocurrency superior to existing non-digital currencies. With transactions theroretically being public, I want to build a small project to possibly guage how transparent the space actually is, peek into the crypto-related activity that celebrities have taken so far, and practice setting up data engineering infrastructure.

**Questions I possibly hope to answer:**
1) Can I see how much a celebrity possibly has within their wallet?
2) Can I track a celebrities activity history and wallet holdings through their transactions?
3) Which celebrities seem the most active within the space?


MVP: Setting up mysql server, ingestion of data through API, and visualization through Metabase.


**Current Architecture:**
![image](https://user-images.githubusercontent.com/24833996/154003470-8119d4fe-4a9a-48b4-85bf-a10a39aafd75.png)
1) Hit Ethplorer API to gather data on Celebrities' Wallet.
2) Connect to Aurora Mysql server on AWS
3) Connect Metabase for data visualization. Hosted on AWS Elastic Beanstalk.

**ERD**

![image](https://user-images.githubusercontent.com/24833996/154002857-11ed3fed-2c7a-4c5c-a79a-06b7fd5c6d7f.png)


**Architecture Improvement Ideas:**
![image](https://user-images.githubusercontent.com/24833996/154005398-02ccd16a-18d9-4552-a4f0-d9ea58017e2a.png)
1) Airlfow for ingestration and transformation orchestration
2) Airbyte to make ingestion simpler
3) DBT for transformations as I get more data to work with.


**Data / Feature Improvement Ideas**:
1) Track more types of blockchains (Bitcoin, Solana, etc)
2) Alerts on transactions or large changes
3) Track NFTs
