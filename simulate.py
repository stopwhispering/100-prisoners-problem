from prisoners.main import main

if __name__ == '__main__':
    main(n_prisoners=100, n_simulations=200, strategy="random", verbose=False)
    main(n_prisoners=100, n_simulations=200, strategy="loop", verbose=False)