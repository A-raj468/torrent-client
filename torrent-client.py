import sys
import time

import libtorrent as lt


def download_torrent(source, save_path="."):
    ses = lt.session({"listen_interfaces": "0.0.0.0:6881"})
    settings = ses.get_settings()
    settings["enable_dht"] = True  # Enable DHT
    ses.apply_settings(settings)

    if source.startswith("magnet:?xt="):
        # Handle magnet link
        params = lt.parse_magnet_uri(source)
    else:
        # Handle .torrent file
        info = lt.torrent_info(source)
        params = lt.add_torrent_params()
        params.ti = info

    params.save_path = save_path
    handle = ses.add_torrent(params)
    print("Fetching metadata, please wait...")

    while not handle.status().has_metadata:
        time.sleep(1)

    print("Metadata retrieved, starting download:", handle.name())

    while not handle.status().is_seeding:
        s = handle.status()
        print(
            "\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s"
            % (
                s.progress * 100,
                s.download_rate / 1000,
                s.upload_rate / 1000,
                s.num_peers,
                s.state,
            ),
            end=" ",
        )

        alerts = ses.pop_alerts()
        for a in alerts:
            if a.category() & lt.alert.category_t.error_notification:
                print(a)

        sys.stdout.flush()
        time.sleep(1)

    print("\nDownload complete:", handle.name())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        torrent_source = sys.argv[1]  # Use command-line argument as torrent file
    else:
        torrent_source = input("Enter magnet link: ").strip()

    download_torrent(torrent_source)
