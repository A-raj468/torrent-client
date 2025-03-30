import time

import libtorrent as lt
from tqdm import tqdm


def download_magnet(magnet_link, save_path="."):
    session = lt.session()
    settings = session.get_settings()
    settings["enable_dht"] = True  # Enable DHT
    session.apply_settings(settings)

    print("Adding magnet link...")
    params = lt.parse_magnet_uri(magnet_link)
    params.save_path = save_path
    handle = session.add_torrent(params)

    print("Waiting for metadata...")
    while not handle.status().has_metadata:
        time.sleep(1)

    print("Metadata received, starting download...")

    torrent_info = handle.get_torrent_info()
    torrent_size = sum(f.size for f in torrent_info.files())

    progress_bar = tqdm(
        total=torrent_size, unit="B", unit_scale=True, desc=torrent_info.name()
    )

    while not handle.status().is_seeding:
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
