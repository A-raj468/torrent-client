import time

import libtorrent as lt
from tqdm import tqdm


def download_magnet(magnet_link, save_path="."):
    session = lt.session()
    params = {
        "save_path": save_path,
        "storage_mode": lt.storage_mode_t.storage_mode_sparse,
    }

    print("Adding magnet link...")
    handle = lt.add_magnet_uri(session, magnet_link, params)
    session.start_dht()

    print("Waiting for metadata...")
    while not handle.has_metadata():
        time.sleep(1)

    print("Metadata received, starting download...")

    torrent_info = handle.get_torrent_info()
    torrent_size = sum([f.size for f in torrent_info.files()])

    progress_bar = tqdm(
        total=torrent_size, unit="B", unit_scale=True, desc=torrent_info.name()
    )

    while not handle.is_seed():
        status = handle.status()
        progress_bar.n = int(status.progress * torrent_size)
        progress_bar.refresh()
        time.sleep(1)

    progress_bar.close()
    print("Download complete!")


if __name__ == "__main__":
    magnet_link = "magnet:?xt=urn:btih:ea5e8e0db64a913c563df30e8535cdc2afc2f5fc"
    # magnet_link = input().strip()
    download_magnet(magnet_link)
