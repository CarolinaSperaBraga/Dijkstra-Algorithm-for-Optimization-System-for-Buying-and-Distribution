# Dijkstra Algorithm for Optimization System for Buying and Distribution

# Project Overview

The project revolves around simulating an optimization problem where clients aim to make purchases from different markets. The goal is to determine how clients can complete their shopping in the most efficient way, considering various constraints, such as:

- **Product Availability**: Each market has a limited quantity of products, and clients have specific product needs.
- **Market Location**: The markets and clients are located in different nodes of a graph, where each node represents either a market or a client, and edges represent the paths between them with associated travel costs (distances).
- **Cost of Goods**: Each market has its own prices for the available products, which vary across different markets.
- **Graph Representation**: The problem is modeled as a graph where nodes represent markets and clients, and edges represent the paths between them with associated costs (distances). The goal is to find the most cost-effective path for each client to complete their shopping.

## Purpose

The project simulates how customers can buy products from multiple markets, considering:

- Product quantity and price variations at each market.
- Transportation costs between customers and markets, as well as between different markets.
- Ensuring that clients buy all the products they want, with the possibility of visiting multiple markets if needed.

The system uses **Dijkstra’s algorithm** to find the shortest paths (minimum distance or cost) between markets and customers, and between markets themselves. This ensures that clients travel the shortest distance possible to purchase their required products. The greedy approach is applied to prioritize the purchase of products in markets that offer the lowest prices and the shortest travel distance.

## Key Features

- **Product Purchase**: Clients buy as much as possible from each market until their needs are met or the market runs out of stock.
- **Market Assignment**: The program assigns clients to specific markets based on the shortest path and product availability.
- **Total Spending Calculation**: After purchases, the total spending of each client is calculated, factoring in both the cost of the products and the travel costs.

The final objective is to print the total cost for each client, including the costs associated with traveling between markets and buying products. If a client cannot complete their purchase, the system will notify that the client couldn't acquire all required products.

## Summary

In summary, this project simulates a complex logistics problem where clients optimize both product purchasing and travel routes to minimize costs, using graph theory and optimization algorithms like Dijkstra's.
